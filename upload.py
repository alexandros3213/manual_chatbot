import json

def upload_pdf_pages_as_documents(discovery, project_id, collection_id, pages, base_title="document"):
    results = []
    for page_obj in pages:
        doc = {
            "title": f"{base_title} - page {page_obj['page']}",
            "text": page_obj["text"],
            "page": page_obj["page"]
        }
        resp = discovery.add_document(
            project_id=project_id,
            collection_id=collection_id,
            file=json.dumps(doc),
            filename=f"{base_title}_page{page_obj['page']}.json",
            file_content_type="application/json"
        ).get_result()
        results.append(resp)
    return results
