%% @author author <author@example.com>
%% @copyright YYYY author.

%% @doc Callbacks for the mydemo application.

-module(mydemo_app).
-author('author <author@example.com>').

-behaviour(application).
-export([start/2,stop/1]).


%% @spec start(_Type, _StartArgs) -> ServerRet
%% @doc application start callback for mydemo.
start(_Type, _StartArgs) ->
    mydemo_sup:start_link().

%% @spec stop(_State) -> ServerRet
%% @doc application stop callback for mydemo.
stop(_State) ->
    ok.
