"""

Design pattern: 
"The Function Manager with raised exceptions 
bubbling up to the parent function"

*******************************
This is useful when you want to split up the code in 
multiple functions, and when you want any raised exception
to bubble up to the very first function (parent) that 
called all the others "in chain" so to speak.

This means that you do not have to manually 
catch exceptions, as any exception will automatically
bubble up to the parent, its error information 
(exception as string) and error context (the traceback) 
will automatically be collected.

At the very first caught exception, the whole 
program flow will interrupt exactly where it is
and sort of "bubble up" to the surface until 
the parent function is reached.

Thus, it is guaranteed that if the very next line of code
is reached, it's because there were no previously 
uncaught exceptions.

Note: the semantics of parent/child is not accurate; 
for the moment this semantic has been given 
until a better one is found.
*******************************


- Giuseppe tavella
"""

import traceback

ctx = {
  "parent_passed": False,
  "reached_end": False,
  "msg_errors": [],
  "ctx_errors": []
}



def func_manager(curr_func):
  def new_curr_func(ctx, *args, **kwargs):
    
      if ctx["reached_end"]:
        ctx["parent_passed"] = False
        ctx["msg_errors"] = []
        ctx["ctx_errors"] = []
        ctx["reached_end"] = False
        
      msgerr = None
      ctxerr = None
      # this is local, is reset for each function frame
      is_this_parent_func = False

      # by reference, persists across function frames
      if not ctx["parent_passed"]:
          # once you set this true, it will be true
          # only for each function frame 
          is_this_parent_func = True
          # once you set this true, it will be true
          # as long as the program lives 
          ctx["parent_passed"] = True

      try:    
        # execute the specific child or parent function
        # (you don't know if it's one or the other)
        curr_func(ctx, *args, **kwargs)
    
      except Exception as e:
        # if this is not the very first function (parent)
        # that invoked all the others (children) 
        # then re-raise the exception so it can 
        # bubble up and will be caught by the parent
        if not is_this_parent_func:
          raise e
        msgerr = str(e)
        ctxerr = traceback.format_exc()

      finally:
        # only run this code once: when the local
        # variable is_this_parent_func will be true, 
        # which means this is the parent function
        if is_this_parent_func:
          if msgerr is not None:
            ctx["msg_errors"].append(msgerr)
            ctx["ctx_errors"].append(ctxerr)
            
          print("first (parent):", curr_func.__name__)
          ctx["reached_end"] = True
        # this is for all children functions
        else:
          # print("last child:", curr_func.__name__)
          pass

  return new_curr_func



@func_manager
def child1(ctx):
  print("in child 1")
  # raise Exception("exception in child1")
  child2(ctx)


@func_manager
def child2(ctx):
  print("in child 2")
  # raise Exception("exception in child2")
  child3(ctx)



@func_manager
def child3(ctx):
  print("in child 3")
  # raise Exception("exception in child3")
  make_bug(ctx)
  child4(ctx)


@func_manager
def child4(ctx):
  print("in child 4")
  # raise Exception("exception in child4")  
  child5(ctx)


@func_manager
def child5(ctx):
  print("in child 5")
  # raise Exception("exception in child5")



def make_bug(ctx):
  # oopss!!
  1/0




def do_something1():
  print("start doing something 1")
  
  child1(ctx)
  
  if len(ctx["msg_errors"]) > 0:
    print("there were some errors in do something 1")
    print(ctx)
    return

  print("no error in do something 1, congrats!")




def do_something2():
  print("start doing something 2")

  child4(ctx)

  if len(ctx["msg_errors"]) > 0:
    print("there were some errors in do something 2")
    print(ctx)
    return

  print("no error in do something 2, congrats!")


do_something1()
print()
do_something2()
