from fastapi import FastAPI
from fastapi.responses import JSONResponse
from LabelClassification import LabelClassification
import uvicorn, json

app = FastAPI(
    title="Daily sales classification API", description="API for mapping labels"
)
label_classification = LabelClassification()


@app.post("/lineitem")
def lineitem(data: dict):
    dataframes = data["dataframes"]
    lineitems_list = [i["lineitem_desc"] for i in dataframes]
    result: dict = label_classification.initiate(
        lineitems=lineitems_list, pms=data["pms"]
    )

    if result:
        for line_item, category in result.items():
            line_item: str = line_item

            for i in dataframes:
                i: dict = i
                line_item_desc: str = i.get("lineitem_desc", "")
                if line_item_desc.lower() == line_item.lower():
                    i["category"] = category
                    
    print("-------------------------------------------------")
    print(dataframes)
    print("-------------------------------------------------")
    
    return JSONResponse(status_code=200, content=dataframes)


if __name__ == "__main__":
    uvicorn.run("app:app", host="localhost", port=8000, reload=True)
