CREATE INDEX mse_state_idx ON messages (state);
CREATE INDEX mse_hashcode_idx ON messages (hashcode);
CREATE INDEX mse_consumer_idx ON messages (consumer);
CREATE INDEX mse_agent_idx ON messages (agent);
CREATE INDEX mse_consumer_state_idx ON messages (consumer, state);
CREATE INDEX mse_agent_state_idx ON messages (agent, state);
CREATE INDEX mse_agent_consumer_idx ON messages (agent, consumer);
CREATE INDEX mse_agent_consumer_state_idx ON messages (agent, consumer, state);
