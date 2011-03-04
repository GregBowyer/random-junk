-module(processes).
-export([maxout/1]).

%% maxout(N)
%%      Create N processes, then destroy them
%%      See how much time this takes

maxout(N) ->
    Max = erlang:system_info(process_limit),
    io:format("Maximum allowed processes: ~p~n", [Max]),
    statistics(runtime),
    statistics(wall_clock),
    L = for(N, fun() -> spawn(fun() -> wait() end) end),
    {_, Time1} = statistics(runtime),
    {_, Time2} = statistics(wall_clock),
    lists:foreach(fun(Pid) -> Pid ! die end, L),
    U1 = Time1 * 1000 / N,
    U2 = Time2 * 1000 / N,
    io:format("Process spawn time=~p (~p) ms~n", [U1, U2]).

wait() ->
    receive
        die -> void
end.

for(N, Func) -> for_itr(1, N, Func).
for_itr(N, N, Func) -> [Func()];
for_itr(I, N, Func) -> [Func() | for_itr(I+1, N, Func)].

