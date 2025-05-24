import json
from ibm_watson import DiscoveryV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from config import API_KEY, SERVICE_URL, VERSION
from query import ask_question
from PyPDF2 import PdfReader
import time
from upload import upload_pdf_pages_as_documents

# Setup
authenticator = IAMAuthenticator(API_KEY)
discovery = DiscoveryV2(version=VERSION, authenticator=authenticator)
discovery.set_service_url(SERVICE_URL)

# List projects and collections
projects = discovery.list_projects().get_result()["projects"]
project_id = projects[0]["project_id"]
collections = discovery.list_collections(project_id=project_id).get_result()["collections"]
collection_id = collections[0]["collection_id"]

# Extract text page by page
pdf_path = "bmw_x1.pdf"
with open(pdf_path, "rb") as f:
    reader = PdfReader(f)
    pages = []
    for idx, page in enumerate(reader.pages, 1):
        page_text = page.extract_text() or ""
        if page_text.strip():
            pages.append({"page": idx, "text": page_text})

# Upload each page as a document
upload_responses = upload_pdf_pages_as_documents(discovery, project_id, collection_id, pages, base_title="bmw_x1")
print(f"Uploaded {len(upload_responses)} documents (one per page)")

# Wait for indexing
for resp in upload_responses:
    document_id = resp["document_id"]
    print(f" Waiting for document {document_id} to finish indexing...")
    for _ in range(120):
        doc_status = discovery.get_document(
            project_id=project_id,
            collection_id=collection_id,
            document_id=document_id
        ).get_result().get("status")
        print("Status:", doc_status)
        if doc_status == "available":
            print(f" Document {document_id} is indexed and ready!")
            break
        time.sleep(1)
    else:
        raise TimeoutError(f"Document {document_id} was not indexed in time.")

print("✅ All documents indexed. You can now ask questions about your PDF!")
print("Type 'exit' or 'quit' to stop.")

chat_history = []

while True:
    question = input("\nAsk a question: ")
    if question.lower() in ("exit", "quit"):
        print("👋 Exiting. Have a nice day!")
        break

    # Combine context
    context_prompt = ""
    for turn in chat_history[-3:]:
        context_prompt += f"User: {turn['question']}\nBot: {turn['answer']}\n"
    context_prompt += f"User: {question}"

    result = ask_question(discovery, project_id, context_prompt)

    if not result.get("results"):
        print("No answers found.")
        continue

    answer_text = ""
    for doc in result.get("results", []):
        passages = doc.get("document_passages", [])
        if passages:
            answer_text = passages[0]["passage_text"]
            break
        answer_text = doc.get("text", "")[:500]

    print(f"\n💬 Bot: {answer_text}")

    chat_history.append({"question": question, "answer": answer_text})
