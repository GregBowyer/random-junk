-module(my_db_super).
-behaviour(supervisor).

-export([start_link/0]).
-export([init/1, stop/0]).

start_link() ->
    supervisor:start_link({local, ?MODULE}, ?MODULE, []).

stop() ->
    exit(whereis(?MODULE), shutdown).

%%
%% Testing a kill can be done totally externally to the 
%% process under supervision by sending it an exit signal
%% e.g. exit(whereis(PID_NAME), KILL_REASON)
%%  → i.e. exit(whereis(my_db), death)

init(_Args) ->
    {ok, {{one_for_one, 2, 3600}, 
          [{my_db, {my_db, start_link, []},
                  permanent, brutal_kill, worker, [my_db]}]}}.

