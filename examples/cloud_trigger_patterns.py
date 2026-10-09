"""Reference-only cloud trigger patterns.

These functions are not registered by the local course application. They show
the Python v2 decorator shape without requiring Azure accounts or credentials.
"""

import logging

import azure.functions as func


cloud_patterns = func.Blueprint()


@cloud_patterns.function_name(name="EventGridPattern")
@cloud_patterns.event_grid_trigger(arg_name="event")
def event_grid_pattern(event: func.EventGridEvent) -> None:
    logging.info("Event Grid subject: %s", event.subject)


@cloud_patterns.function_name(name="EventHubsPattern")
@cloud_patterns.event_hub_message_trigger(
    arg_name="events",
    event_hub_name="%EVENT_HUB_NAME%",
    connection="EventHubConnection",
    cardinality="many",
    consumer_group="$Default",
)
def event_hubs_pattern(events: list[func.EventHubEvent]) -> None:
    logging.info("Received %d Event Hubs events.", len(events))


@cloud_patterns.function_name(name="ServiceBusPattern")
@cloud_patterns.service_bus_queue_trigger(
    arg_name="message",
    queue_name="%SERVICE_BUS_QUEUE%",
    connection="ServiceBusConnection",
)
def service_bus_pattern(message: func.ServiceBusMessage) -> None:
    logging.info("Service Bus message ID: %s", message.message_id)


@cloud_patterns.function_name(name="CosmosChangeFeedPattern")
@cloud_patterns.cosmos_db_trigger(
    arg_name="documents",
    database_name="%COSMOS_DATABASE%",
    container_name="%COSMOS_CONTAINER%",
    connection="CosmosConnection",
    lease_container_name="leases",
    create_lease_container_if_not_exists=True,
)
def cosmos_change_feed_pattern(documents: func.DocumentList) -> None:
    logging.info("Received %d changed documents.", len(documents))
