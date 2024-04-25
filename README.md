# CogitoApp
Main monolith app

app/
Business logic for entities. One REST API in container for all entities duting MVP stage

client/
Client folder for telegram bot during MVP and Flutter in future

db/
Managing database (migrations, db structure, data access paths)

llm/
Module for running LLM models and language pipelines

middleware/
auth/ - logic for jwt auth
messanger/ - logic for sending messages to user
sheduler/ - module for processing events pereodic tasks