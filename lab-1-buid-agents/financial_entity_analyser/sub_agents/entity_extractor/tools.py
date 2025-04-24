from .schema import FinancialEntities


def check_entity_names_model(response: dict) -> FinancialEntities:
    """Validates the LLM response.

    Args:
        response (dict): The response returned by `entity_extractor_agent`

    Returns:
        vFinancialEntities: The parsed response of `entity_extractor_agent`
    """

    parsed_response = FinancialEntities(response)

    return parsed_response
