%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% File    : db.erl
%%% Author  : Francesco Cesarini <francesco@erlang-solutions.com>
%%% Purpose : Solution for Exercise 4, sequential programming
%%%           exercises. A database back end module
%%% Created : 10 Jan 2001 by Francesco Cesarini
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
-module(db).
-author('francesco@erlang-solutions.com').
-export([new/0, write/3, delete/2, read/2, match/2, destroy/1]).

%% new() -> list().
%% Create a new database
new() -> 
    [].

%% insert(term(), term(), list()) -> list()
%% Insert a new element in the database
write(Key, Element, []) ->
    [{Key, Element}];
write(Key, Element, [{Key, _} | Db]) ->
    [{Key, Element}|Db];
write(Key, Element, [Current | Db]) ->
    [Current | write(Key, Element, Db)].

%% delete(term(), list()) -> list()
%% Remove an element from the database
delete(Key, [{Key, _Element}|Db]) -> 
    Db;
delete(Key, [Tuple|Db]) ->
    [Tuple|delete(Key, Db)];
delete(_Key, []) ->
    [].

%% lookup(term(), list()) -> {ok, term()} | {error, instance}
%% Retrieve the first element in the database with a matching key
read(Key, [{Key, Element}|_Db]) -> 
    {ok, Element};
read(Key, [_Tuple|Db]) ->
    read(Key, Db);
read(_Key, []) ->
    {error, instance}.

%% match(term(), list()) -> list()
%% Return all the keys whose values match the given element.
match(Element, [{Key, Element}|Db]) -> 
    [Key|match(Element, Db)];
match(Element, [_Tuple|Db]) ->
    match(Element, Db);
match(_Key, []) ->
    [].


%% destroy(list()) -> ok.
%% Deletes the database. 

destroy(_Db) ->
    ok.

