from open_ai.schemas import Model, Cost


models = [
    Model(name='gpt-4.1-2025-04-14',
          short_name='gpt-4.1',
          cost=Cost(input=2.00, cached_input=0.50, output=8.00)),
    Model(name='gpt-4.1-nano-2025-04-14',
          short_name='gpt-4.1-nano',
          cost=Cost(input=0.10, cached_input=0.025, output=0.40)),
]
