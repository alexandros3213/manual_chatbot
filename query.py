def ask_question(discovery, project_id, question, count=3):
    response = discovery.query(
        project_id=project_id,
        natural_language_query=question,
        count=count
        # return_fields is not supported in Discovery V2
    ).get_result()
    return response
