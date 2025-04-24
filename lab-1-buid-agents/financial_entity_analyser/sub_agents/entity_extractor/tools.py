import time
import os
from google.cloud import bigquery
from vertexai import rag

from .schema import FinancialEntities

def check_bq_models(dataset_id: str) -> str:
    """Lists models in a BigQuery dataset and returns them as a string.

    Args:
        dataset_id: The ID of the BigQuery dataset (e.g., "project.dataset").

    Returns:
        A string representation of a list of dictionaries, where each dictionary
        contains the 'name' and 'type' of a model in the specified dataset.
        Returns an empty string "[]" if no models are found.
    """

    try:
        client = bigquery.Client()

        models = client.list_models(dataset_id)
        model_list = []  # Initialize as a list

        print(f"Models contained in '{dataset_id}':")
        for model in models:
            model_id = model.model_id
            model_type = model.model_type
            model_list.append({"name": model_id, "type": model_type})

        return str(model_list)

    except Exception as e:
        return f"An error occurred: {str(e)}"


def execute_bqml_code(bqml_code: str, project_id: str, dataset_id: str) -> str:
    """
    Executes BigQuery ML code.
    """

    # timeout_seconds = 1500

    client = bigquery.Client(project=project_id)

    try:
        query_job = client.query(bqml_code)
        start_time = time.time()

        while not query_job.done():
            elapsed_time = time.time() - start_time
            # if elapsed_time > timeout_seconds:
            #     return (
            #         "Timeout: BigQuery job did not complete within"
            #         f" {timeout_seconds} seconds. Job ID: {query_job.job_id}"
            #     )

            print(
                f"Query Job Status: {query_job.state}, Elapsed Time:"
                f" {elapsed_time:.2f} seconds. Job ID: {query_job.job_id}"
            )
            time.sleep(5)

        if query_job.error_result:
            return f"Error executing BigQuery ML code: {query_job.error_result}"

        if query_job.exception():
            return f"Exception during BigQuery ML execution: {query_job.exception()}"

        results = query_job.result()
        if results.total_rows > 0:
            result_string = ""
            for row in results:
                result_string += str(dict(row.items())) + "\n"
            return f"BigQuery ML code executed successfully. Results:\n{result_string}"
        else:
            return "BigQuery ML code executed successfully."

    except Exception as e:
        return f"An error occurred: {str(e)}"


def check_entity_names_model(response: dict) -> FinancialEntities:
    """Validates the LLM response.

    Args:
        response (dict): The response returned by `entity_extractor_agent`

    Returns:
        vFinancialEntities: The parsed response of `entity_extractor_agent`
    """

    parsed_response = FinancialEntities(response)

    return parsed_response
