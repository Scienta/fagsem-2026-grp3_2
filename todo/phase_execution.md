
# Executing according to a plan

Before starting, make sure that the plan has the following features:

1. A list of phases or steps at the start, formatted as a todo-list
   with check boxes

If this is missing, analyse the steps, and create the list. The list should
take into account dependencies between tasks, and make sure the order is
the optimal implementation sequence.

## Phase Execution

When executing a plan, do as follows:

1. Identify the first non-checked item in the checklist
2. Follow the recipe in the plan for that item
3. When completed, add at least one test for the new function
4. When the new and old tests all run WITHOUT WARNINGS,
   check off the item in the checklist, and commit the changes to git.
5. Check the status of the context window.
   If tokens > 130000, stop and report to the human.
   If tokens < 130000, move to the next item on the list.
6. **Don't stop** until either you have executed all the phases in the
   plan, or the token count exceeds the given limit.
