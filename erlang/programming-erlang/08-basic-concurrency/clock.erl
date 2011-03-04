-module(clock).
-export([start/2, stop/0]).

start(Time, Func) ->
    register(clock, spawn(fun() -> tick(Time, Func) end)).

stop() -> clock ! stop.

tick(Time, Func) ->
    receive
        stop -> void
    after Time ->
            Func(),
            tick(Time, Func)
end.


