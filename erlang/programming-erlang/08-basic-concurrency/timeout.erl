-module(timeout).
-export([timeout/1]).

sleep(Time) ->
    receive
    after Time -> true
end.

flush_buffer() ->
    receive
        _Any -> flush_buffer()
    after 0 ->
        true
end.

timeout(T) -> sleep(T).
