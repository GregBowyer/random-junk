-module(misc).
-export([apply_test/0, apply_test2/0, attr_test/0, 
        block_statement/0, block_statement2/0,
        list_operation/2, list_operation2/2]).
-vsn(1.1).

-author("User defined attribute").

apply_test() -> apply(erlang, atom_to_list, [hello]).
apply_test2() -> apply(fun(X) -> X*X end, [100]).

attr_test() -> misc:module_info().

block_statement() ->
    begin
        io:format("First statement \n"),
        io:format("Second statement \n"),
        io:format("Third statement \n")
    end.

block_statement2() ->
    begin
        A = io:format("First statement \n"),
        B = io:format("Second statement \n"),
        C = io:format("Third statement \n"),

        {A,B,C}
    end.
        
list_operation(L1, L2) ->
    L1 ++ L2.

list_operation2(L1, L2) ->
    L1 -- L2.
