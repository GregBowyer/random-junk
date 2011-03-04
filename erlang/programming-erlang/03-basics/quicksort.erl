-module(quicksort).
-export([qsort/1]).

qsort([]) -> [];
qsort([Pivot | Cdr]) ->
    qsort([X || X <- Cdr, X < Pivot])
    ++ [Pivot] ++
    qsort([X || X <- Cdr, X >= Pivot]).
