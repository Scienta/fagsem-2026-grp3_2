
# Introduction

The goal of this project is to create a tax calculator.

This file contains general directions on how development shall be done.

The file serves mainly as base instructions for coding agents.

## Git

The code is version controlled in git.

Remember to use the adaquate git file commands when moving/renaming/deleting files etc.

## Environment

The project uses a virtual environment (.venv).
When starting, check that the venv is activated. **Otherwise, tell the human
that it needs to be activated, and stop executuion.**

The running shell shall be set up with PYTHONPATH=${PWD}/src
**If this not the case, stop execution and inform the human.**

All dependencies shall be registered in `requirements.txt` and installed in the venv
using `pip`.

**IMPORTANT:** You will be given a sub-folder where you should do your work.
Refrain from editing not inside the sub-folder, with the exception of `requirements.txt`.
_NEVER_ remove anything from `requirements.txt`.


### Important Note

Since the venv and the PYTHONPATH are set, don't set these explicitely when running tools
and processes, this only causes unnecessary permission requests. Just run the command without
the PYTHONPATH and venv in the invocation.

## Running `bash` commands

* When running `bash` commands, avoid newlines and comments in the command, as it causes an approval request
  to the human, effectively halting execution until an approval arrives.
* Do not use `${}` constructs in bash commands, as this triggers human approval
* Do not use newline or comments in code snippets to execute, as this trigger human approval
* For python commands, use either `python` or `.venv/bin/python` -- do not use the absolute path, since this
  triggers human approval requests.

## Planning

When planning how to implement a feature or complete a task, follow the instructions
in `todo/making_a_plan.md`, and when following the plan, follow the instructions in
`todo/phase_execution.md`.

## Testing

Create tests for code that you generate. We use `pytest`, and place tests in `test/`.
Since `pytest-xdist` is installed, you can run tests in parallel with `-n auto` in order to
speed up execution.

### More comprehensive tests

For more comprehensive tests that take a long time to run, place these in the `regtest` directory.
For these tests, shell scripts are just as welcome as tests run through `pytest`

## No Broken Windows

When you have made changes to files, always run all the tests afterwards to verfy functionality.

Before finishing, make sure all tests run and that there are

* NO FAILING TESTS
* NO WARNINGS
