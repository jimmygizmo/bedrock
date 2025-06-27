
## Bedrock - Optional Components

#### =============

### COMING SOON: Documentation on the included Jupyter Notebook Server

### COMING SOON: Documentation on the included pgAdmin DB GUI Server

Both of these extremely powerful services are pre-configured in the Bedrock stack. To use either or both with
Bedrock, simply uncomment the corresponding section(s) in the docker-compose.yml file. Any credentials or
secrets you need for either service are visible in the docker-compose.yml.

Both the Jupyter Notebook server and pgAdmin server containers are relatively large and time-consuming builds.
Bedrock with only the FastAPI container and PostgreSQL container builds very quickly and is not very large. Also,
pgAdmin is not likely to be part of a normal production deployment to a DMZ or the equivalent.

Both the Jupyter and pgAdmin services are more likely to be used internally, for development, research or
experimentation or deployed as an internal-only service, maybe along with a Bedrock-derived enterprise app,
but not a public facing consumer stack as such. Still, it is very valuable to include these pre-configured
stack components, and others I have in development.

Bedrock is like a Swiss Army Knife with a huge spectrum of capabilities, but performant
and modular, so you can do almost anything and do it extremely well, but you can also do it efficiently,
in a lean and mean configuration when the context requires that.


---------------------------------------------------------------------------

This project has been authored, engineered and developed by James Mannix with both original and open source components.

 More information at: [SmartMetal.ai](http://smartmetal.ai/ "SmartMetal.ai")

This project is licensed under the [MIT License](./LICENSE.txt).


#### Copyright (c) 2025 James Mannix, SmartMetal.ai

---------------------------------------------------------------------------

