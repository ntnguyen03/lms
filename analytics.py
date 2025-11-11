import pandas as pd
from typing import Optional, Dict, Any


def load_sales_data_summary(excel_path: str) -> Optional[Dict[str, Any]]:
    try:
        df = pd.read_excel(excel_path)
        if df.empty:
            return None
        summary = {
            'num_rows': int(len(df)),
            'columns': list(df.columns.astype(str)),
        }
        # If numeric columns exist, compute simple totals/means
        numeric_df = df.select_dtypes(include='number')
        if not numeric_df.empty:
            summary['totals'] = numeric_df.sum().round(2).to_dict()
            summary['means'] = numeric_df.mean().round(2).to_dict()
        return summary
    except Exception:
        return None


