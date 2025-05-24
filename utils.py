import time

def wait_for_document_indexing(discovery, project_id, collection_id, document_id, timeout=60):
    print("⏳ Waiting for document to finish indexing...")
    for _ in range(timeout):
        status = discovery.get_document(
            project_id=project_id,
            collection_id=collection_id,
            document_id=document_id
        ).get_result()
        
        doc_status = status.get("status")
        print(f"Status: {doc_status}")
        
        if doc_status == "available":
            print("✅ Document is indexed and ready!")
            return
        time.sleep(1)
    
    raise TimeoutError("Document was not indexed in time.")
