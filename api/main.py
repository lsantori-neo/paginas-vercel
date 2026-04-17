from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
import io
import json
import base64
from typing import List

app = FastAPI()

# CORS configuration for Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/reconcile")
async def reconcile(
    file_a: UploadFile = File(...),
    file_b: UploadFile = File(...),
    key_cols: str = Form(...),
    compare_cols: str = Form(...)
):
    """
    Main reconciliation endpoint
    key_cols: JSON string of column names to use as keys
    compare_cols: JSON string of column names to compare
    """
    try:
        # Parse input
        key_cols = json.loads(key_cols)
        compare_cols = json.loads(compare_cols)
        
        # Read files
        file_a_content = await file_a.read()
        file_b_content = await file_b.read()
        
        if file_a.filename.endswith('.xlsx'):
            df_a = pd.read_excel(io.BytesIO(file_a_content))
        else:
            df_a = pd.read_csv(io.BytesIO(file_a_content))
        
        if file_b.filename.endswith('.xlsx'):
            df_b = pd.read_excel(io.BytesIO(file_b_content))
        else:
            df_b = pd.read_csv(io.BytesIO(file_b_content))
        
        # Validation
        if df_a.empty or df_b.empty:
            return JSONResponse(
                status_code=400,
                content={"error": "Uno o ambos archivos están vacíos"}
            )
        
        # Check columns exist in both tables
        missing_in_b = [col for col in key_cols if col not in df_b.columns]
        if missing_in_b:
            return JSONResponse(
                status_code=400,
                content={"error": f"Columnas de cruce no existen en Tabla B: {', '.join(missing_in_b)}"}
            )
        
        # RECONCILIATION LOGIC
        df_merge = pd.merge(df_a, df_b, on=key_cols, how='outer', suffixes=('_A', '_B'), indicator=True)
        
        # Separate results
        coincidencias = df_merge[df_merge['_merge'] == 'both'].copy()
        solo_a = df_merge[df_merge['_merge'] == 'left_only'].copy()
        solo_b = df_merge[df_merge['_merge'] == 'right_only'].copy()
        
        # Detect differences
        diferencias = pd.DataFrame()
        diferencias_detalle = []
        
        if compare_cols:
            compare_cols_valid = [col for col in compare_cols if col in df_b.columns]
            
            if compare_cols_valid:
                for idx, row in coincidencias.iterrows():
                    diff_cols = []
                    for col in compare_cols_valid:
                        val_a = row.get(f"{col}_A")
                        val_b = row.get(f"{col}_B")
                        
                        if pd.isna(val_a) and pd.isna(val_b):
                            continue
                        elif pd.isna(val_a) or pd.isna(val_b):
                            diff_cols.append(col)
                        elif str(val_a).strip() != str(val_b).strip():
                            diff_cols.append(col)
                    
                    if diff_cols:
                        row_data = {col: row[col] for col in key_cols}
                        row_data['Columnas_con_diferencias'] = ', '.join(diff_cols)
                        for col in diff_cols:
                            row_data[f"{col}_A"] = row.get(f"{col}_A")
                            row_data[f"{col}_B"] = row.get(f"{col}_B")
                        diferencias_detalle.append(row_data)
                
                if diferencias_detalle:
                    diferencias = pd.DataFrame(diferencias_detalle)
        
        # Clean up data for JSON response
        coincidencias_clean = coincidencias.drop(columns=['_merge'], errors='ignore')
        solo_a_clean = solo_a.drop(columns=['_merge'], errors='ignore')
        solo_b_clean = solo_b.drop(columns=['_merge'], errors='ignore')
        
        # Generate Excel file and encode to base64
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_a.to_excel(writer, index=False, sheet_name='Tabla A Original')
            df_b.to_excel(writer, index=False, sheet_name='Tabla B Original')
            coincidencias_clean.to_excel(writer, index=False, sheet_name='Coincidencias')
            solo_a_clean.to_excel(writer, index=False, sheet_name='Solo en A')
            solo_b_clean.to_excel(writer, index=False, sheet_name='Solo en B')
            if not diferencias.empty:
                diferencias.to_excel(writer, index=False, sheet_name='Diferencias')
        
        output.seek(0)
        excel_data = base64.b64encode(output.getvalue()).decode('utf-8')
        
        # Prepare response
        return {
            "status": "success",
            "summary": {
                "coincidencias": int(len(coincidencias_clean)),
                "solo_a": int(len(solo_a_clean)),
                "solo_b": int(len(solo_b_clean)),
                "diferencias": int(len(diferencias))
            },
            "data": {
                "coincidencias": coincidencias_clean.head(10).to_dict(orient='records'),
                "solo_a": solo_a_clean.head(10).to_dict(orient='records'),
                "solo_b": solo_b_clean.head(10).to_dict(orient='records'),
                "diferencias": diferencias.head(10).to_dict(orient='records')
            },
            "excel_base64": excel_data
        }
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Error en procesamiento: {str(e)}"}
        )
