-module(stimer).
-export([timer/2, cancel/1, start/2]).

timer(Time, Fun) ->
    receive
        cancel -> void
    after Time ->
            Fun()
end.

start(Time, Fun) -> spawn(fun() -> timer(Time, Fun) end).

cancel(Timer) -> Timer ! cancel.
