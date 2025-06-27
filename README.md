
## Bedrock

#### =============

### A Premium Python FastAPI Full Stack, Fully Loaded

#### *The simplest, fastest, best-practice way to build an advanced full-stack solution.*

---------------------------------------------------------------------------

#### ✅ Fastest FastAPI Possible (the only fully asynchronous Python stack)

#### ✅ Best-practice Python design patterns featuring Dependency Injection

#### ✅ Clean FastAPI architecture: models, schemas, routers, services, core

#### ✅ Includes 11 table ERP DB with complete CRUD API and rich mock data

#### ✅ Unit and integration tests for advanced FastAPI with coverage reports

#### ✅ Automatic API docs & tools via both OpenAPI (aka Swagger) and Redocly

#### ✅ The best-engineered stack available for both web applications & microservices

#### ✅ Latest PostgreSQL 17.2 RDBMS with pgAdmin 8.14 IDE (Pro DB Admin GUI)

#### ✅ Pydantic data validation - full coverage, with matching PyTest unit tests

#### ✅ Optional loaded Jupyter Notebook Server with .ipynb apps for this FastAPI

#### ✅ Secret separation: clean, secure. Convenient for developers, safe for the repo

#### ✅ MIT License. Only requires attribution. Only prohibits re-distribution.

---------------------------------------------------------------------------

### Numerous powerful features are nearly ready for release and coming soon!

The following powerful modules and features are all completely or mostly mature in the prototype stack and
ready for release. Most or all will be added to Bedrock revisions here in June 2025. Everything is under
the same MIT License. This is all totally free and Open Source.

### 🔐 Authentication and Single Sign On (SSO) with JWT, OAuth 2 and more

### 🧱 Application building-block API endpoints with roles-base authorization

### 🚀 NGINX 1.23 Reverse Proxy and Accelerator Cache (fastest static content delivery)

### 🗝️ NGINX SSL/Security configuration: Highest-possible rating of A++

### 🔥 Redis cache, message queue and NoSQL store for acceleration, async processing

### 🛢️ Alembic for DB Migrations and high-quality mock-data seeding; developer friendly

### 🖥️ Premium React front end: TypeScript, React Router, Redux, Material UI

### 🧠 Integration with Serverless PAAS like RunPod GPUs for AI/ML workloads

### ☁️ AWS automation for Bedrock: Create, configure VMs. Deploy Bedrock easily

### 🌐 GIS support in the DB and in GIS Magma modules for geospatial apps

### 🔌 Bedrock speaks REST by default but WebSocket and GraphQL modules are coming

### 💰 All free. All expertly crafted and integrated by a 20-year professional developer

---------------------------------------------------------------------------

## Quick Set Up

### Clone the repository and then cd into it.

You are now in the 'project root'. Most commands and actions, if not otherwise specified, should be done from this
directory. The project root is the directory with docker-compose.yml in it.

    git clone git@github.com:jimmygizmo/bedrock.git

    cd bedrock

### Increase some directory permissions for database storage

(Needed for Windows WSL for sure and possibly others.) This command will give full permissions to the /dbvolume/
directory where the large DB file structure will be written by the PostgreSQL DB. You might have reasons later
to do something similar again and you might in some cases need to use sudo. This is needed because the docker process behind
Postgres is running at an elevated level. WSL handles this worse than macOS or Linux. Note that it is useful to
completely wipe out all persisted DB data to cause the DB to be re-created fresh, sometimes frequently, and this
is when you will most likely need those permissions. (I'll cover DB wiping during dev later.)

    sudo chomd -R 777 dbvolume 

---------------------------------------------------------------------------

## Start The Bedrock Stack

On the first startup, Magma (the FastAPI Microservices Python app) will create all the database objects
including the logical database itself, if necessary. The stack should work immediately. If not, simply restart it.

    docker-compose up
    
    *NEW* Scroll down and read about the new Bedrock Developer Menu (menu.py), which automates such actions!

>  ***Optional: Jupyter Notebook Server, pgAdmin DB GUI*** - For quick and efficient core stack builds out of the box,
> the pre-configured Jupyter and pgAdmin components are disabled in the docker-compose.yml file by default. To use
> either or both with Bedrock, simply uncomment the corresponding Docker  Compose service block.
> For more information, see: [Optional Bedrock Components](./extras/MORE.md)

### Operate the API and auto-generated API documentation (OpenAPI and Redocly)

You access port 48000 on localhost, since we map the default FastAPI port 8000 to 48000 outside the container.
Bedrock always uses ports in the 40-thousand ranges when mapping outside the Compose stack:
5432 -> 45432. 443 -> 44443, 8000 -> 48000, 80 -> 44080, etc.

> **Note**: When internal service ports are mapped to 'Bedrock' ports outside the container, the mneumonic
> used is to first choose a similar 44*** port number and then a 40*** number before other 4****
> numbers to find the best mapping. Bedrock has many potential modules so this scheme will be used to make
> sense of potentially many port numbers in a complex stack.


    For OpenAPI interactive docs and API tools, navigate to:
    https://127.0.0.1:48000/docs

    For Redocly interactive docs, navigate to:
    https://127.0.0.1:48000/redoc


### Use your Browser to explore the "Magma" API Endpoints

For a full list of endpoints and more information about the Magma FastAPI application at the core of the
Bedrock stack, please read [Bedrock Magma API](./extras/API.md). Bedrock is a Python FastAPI platform and Magma
is the rich, modern, best-practice code base to use as your API starting point.

Magma features over 40 CRUD endpoints for the rich ERP database schema and mock data set "Chinook" which is
the basis for an online music store like iTunes. Chinook has a relational schema of medium complexity with
circular relations and other advanced characteristics to give you a real-world foundation to learn from
and build your own enterprise solution upon. Basic endpoints are provided for all 11 tables. A few examples:


    List all music tracks using paging parameters:
    http://localhost:48000/tracks/?skip=0&limit=100

    List all artists:
    http://localhost:48000/artists

    Get the playlist with playlist_id 3:
    http://localhost:48000/playlists/3

    * See the "Bedrock Magma API" link above (the extras/API.md file) or the built-in OpenAPI docs/tools for details.

### Shut down the stack

    hit ctrl-C    (in the same console)
    
    *NEW* Scroll down and read about the new Bedrock Developer Menu (menu.py), which automates such actions!

#### Visit [SmartMetal.ai](http://smartmetal.ai/ "SmartMetal.ai") for more information.
#### The Bedrock Stack is the foundation on which SmartMetal.ai is built.

---------------------------------------------------------------------------

## Development Environment

This section will soon get a lot of detailed and valuable information for Bedrock developers.

I use Pyenv for my virtual environments and this project containers a .python-version file specifying a virtual
environment from Pyenv with the name 've.bedrock' so I recommend you use all that and will provide good
instructions soon.

When you create ve.bedrock with Pyenv you want to use Python version 3.10.9 to match the Python image Bedrock uses
in the running container. (see bedrock/Dockerfile). You will want to use the requirements-pinned.txt file so that
all of your module versions in your local development environemt matches those in your deployed app.

    > pyenv install 3.10.9

    > pyenv virtualenv 3.10.9 ve.bedrock

    For the best Python installs/upgrades, always upgrade pip and setuptools in a fresh virtual environment.

    > pip install --upgrade pip
    > pip install --upgrade setuptools

    Install the large number of dependencies.

    > pip install -r requirements-pinned.txt

    Install the application module Magma itself.
    First cd into the bedrock container directory so you are in the same directory as setup.py
    You should then be inside /bedrock/bedrock/ (one-level deeper than the repo root of /bedrock/

    > cd bedrock
    > pip install .

This is important for running your Python code locally, outside of Docker, but it is equally important so your
powerful IDE with real-time analysis (such as PyCharm or VS Code) will operate properly and to its fullest potential.

I'm a hardcore developer and this project is for developers so you can expect this to be a rich and valuable section
of the docs for this project. I have a lot of strategic and tactical knowlege to pass on through this and other
projects of mine, especially with regards to architecture and development. It's all about the code so stay tuned for
lots of updates to this repo coming soon, valuable to my fellow developers most of all.

---------------------------------------------------------------------------

## Bedrock Developer Menu - menu.py

The Bedrock Developer Menu is a really slick little tool which displays the colorful combined docker log for
all containers while giving you a menu of single keypress command macros for your most common and repetitive
development actions. These are the handful of command sequences a full stack developer types into a terminal
constantly, sometimes over a hundred times in a day. Having these under a single keypress is a wonderful
benefit. A tiny but incredibly valuable addition to Bedrock: menu.py

- 1 - Start the Bedrock full stack & Magma microservices
- 2 - Stop the entire stack
- 3 - Delete the entire logical DB and all data
- 4 - Rebuild the Bedrock FastAPI container with current Magma code
- 5 - Run unit tests
- 6 - Reinstall the FastAPI microservices module 'magma' locally
- 7 - Git status
- 8 - Exit menu only (stack up/down state will not change)

---------------------------------------------------------------------------

## Extensive Documentation, Guides, Tutorials

#### 🔥 *Extensive documentation is under development and coming soon!*

### Chinook ERP Database Schema

NOTE: Diagram shows PascalCase naming, which is supported in Magma through aliasing, making imports of the substantial
Chinook mock data simpler. However other than the aliases, all DB objects are referenced pythonically and per DB/ORM
best practices and use lowercase_underscore naming and plural table names, with singlular model-related object names.
A more accurate diagram is pending.

![Diagram](./extras/erp-schema-chinook.png)

A lot more documentation is on the way. The project is currently well structured, clean and largely self-documenting,
so don't delay in starting to build your amazing projects on Bedrock!


---------------------------------------------------------------------------

## License

This project has been authored, engineered and developed by James Mannix with both original and open source components.

 More information at: [SmartMetal.ai](http://smartmetal.ai/ "SmartMetal.ai")

This project is licensed under the [MIT License](./extras/LICENSE.txt).

- ✅ Free to use, modify, and distribute
- ✅ Commercial use allowed
- ✅ Attribution required (include the license and copyright)
- ❌ No warranty (use at your own risk)
- ❌ No re-packaging/re-distribution as a full-stack template
- ✅ Distribute and profit from your custom solutions with no restrictions

#### Copyright (c) 2025 James Mannix, SmartMetal.ai

---------------------------------------------------------------------------

