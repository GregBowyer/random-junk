%% @author author <author@example.com>
%% @copyright YYYY author.

%% @doc Callbacks for the que application.

-module(que_app).
-author('author <author@example.com>').

-behaviour(application).
-export([start/2,stop/1]).


%% @spec start(_Type, _StartArgs) -> ServerRet
%% @doc application start callback for que.
start(_Type, _StartArgs) ->
    que_sup:start_link().

%% @spec stop(_State) -> ServerRet
%% @doc application stop callback for que.
stop(_State) ->
    ok.
