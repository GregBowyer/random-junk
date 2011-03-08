%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% File    : my_db.erl
%%% Author  : Francesco Cesarini <francesco@erlang-solutions.com>
%%% Purpose : Solution Exercise 1, Process Design Patterns
%%%           A Database server
%%% Created : 25 Apr 2001 by Francesco Cesarini
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
-module(my_db).
-author('francesco@erlang-solutions.com').

%% Internal Exports
-export([init/1, handle_call/3, handle_cast/2, terminate/2]).

%%External Exports
-export([start_link/0, start/0, stop/0, write/2, delete/1, dump/0, read/1, match/1]).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Client Functions
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

start_link() ->
    start().

%% start() -> ok.
%% Starts the database server
start() ->
    gen_server:start_link({local, my_db}, my_db, [], []).

%% stop() -> ok.
%% Stops the database server
stop() ->
    gen_server:cast(my_db, {stop}).

%% write(term(), term()) -> ok.
%% Inserts an element in the database server
write(Key, Element) ->
    gen_server:cast(my_db, {write, Key, Element}).

%% delete(term()) -> ok.
%% Removes an element from the database. Will succeed even
%% If the element does not exist.
delete(Key) ->
    gen_server:cast(my_db, {delete, Key}).

%% read(term()) -> {ok, term()} | {error, instance}
%% Will retrieve an element from the database.
read(Key) ->
    gen_server:call(my_db, {read, Key}).

dump() ->
    gen_server:call(my_db, dump).

%% match(term()) -> [term()] | []
%% Will return a list of keys which match to the element
%% sent in.
match(Element) ->
    gen_server:call(my_db, {match, Element}).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Database Server Loop
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% init() 
%% Initialises the database and enters the server loop
init(_Args) ->
    {ok, db:new()}.

handle_call(dump, _From, Db) ->
    {reply, Db, Db};
handle_call({read, Key}, _From, Db) ->
    {reply, db:read(Key, Db), Db};
handle_call({match, Query}, _From, Db) ->
    {reply, db:match(Query, Db), Db}.

handle_cast({write, Key, Element}, Db) ->
    NewDb = db:write(Key, Element, Db),
    {noreply, NewDb};
handle_cast({delete, Key}, Db) ->
    NewDb = db:delete(Key, Db),
    {noreply, NewDb};
handle_cast(stop, Db) ->
    {stop, normal, Db}.

terminate(normal, Db) ->
    db:destroy(Db),
    ok.
