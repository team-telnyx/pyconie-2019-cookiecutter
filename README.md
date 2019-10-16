# Cookie Cutters

Templates for [Cookiecutter](https://cookiecutter.readthedocs.io/en/latest/)!

In order to create a project from this cookie cutter, you'll need to [install it](https://cookiecutter.readthedocs.io/en/latest/installation.html). Once installed and this repo is cloned locally, you can check out [how to generate a new project](https://cookiecutter.readthedocs.io/en/latest/usage.html#generate-your-project).

## Presentation
The associated presentation can be accessed here: https://docs.google.com/presentation/d/e/2PACX-1vRBJVv2Z4UdFnkv8oJIfUKp-RliLbFU9TGXItqSr3DMdQzNOq-oKSquGe3Z8-sUCNf09t_s_11x3LV0/pub?start=false&loop=false&delayms=3000#slide=id.g5700329f4d_0_783

## Templates

`cookiecutter pyconie-2019-cookiecutter/base`

## User Input

On creation you will be prompted for the following information.
Please take the time to carefully answer these as many of the values will be used in the
service directory to help audit our services.

|Name|Choices|Type|Comments|
| -- | -- | -- | -- |
| event | `PyCon IE 2019` | string | Squad that owns the service |
| primary_maintainer | Name for the primary maintainer | string   | Primary directly responsible individual |
| app_name | dialajoke | string   | Name of the app |
| repo_name | dial-a-joke |  string  | Name of Github repo |
| container_name | dial-a-joke | string   | Unique name of the container (and service) |
| project_short_description | -- | string   | High level summary of the service for the README |

## New Project Workflow

You're starting with a new project created via cookiecutter as above.

* `pip install -r requirements.txt`


* Testing/linting/etc.  [Invoke](http://www.pyinvoke.org/) is included in
  `requirements.txt` and it provides an easier environment than Bash to control
  I/O from testing tools. When running `inv` or `invoke`, Invoke will search
  for a `tasks` module/package and execute commands from it.
  * Available commands: `inv --list`
  * Command details: `inv <command> --help`
