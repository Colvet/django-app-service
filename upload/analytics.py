class MakeSummary:

    def analy(df):
        info = []
        for d in df:
            col_info = {
                "colName": d,
                "nullCount": int(df[d].isnull().sum()),
                "selected": 1,
                "summary": {
                    "dataType": "String",
                    "deIdentified": "masking",
                    "prove": "K"
                }
            }

            info.append(col_info)
        del_null_df = df.dropna(how="any")
        return del_null_df, info
