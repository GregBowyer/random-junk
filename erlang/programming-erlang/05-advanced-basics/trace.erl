-module(trace).
-export([start/0]).

-ifdef(debug).
-define(TRACE(X), io:format("TRACE ~p:~p ~p~n", [?MODULE, ?LINE, X])).
-else.
-define(TRACE(X), void).
-endif.

start() -> loop(5).

loop(0) -> 
    void;
loop(I) ->
    ?TRACE(I),
    loop(I - 1).
