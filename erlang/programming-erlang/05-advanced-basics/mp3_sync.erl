-module(mp3_sync).
-export([find_sync/1]).

find_sync(Bin, N) ->
    case is_header(N, Bin) of
        {ok, Len1, _} ->
            case is_header(N + Len1, Bin) of
                {ok, Len2, _} ->
                    case is_header(N + Len1 + Len2, Bin) of 
                        {ok, _, _} ->
                            {ok, N}
                        error ->
                            find_sync(Bin, N+1)
                    end;
                error ->
                    find_sync(Bin, N+1)
            end;
        error ->
            find_sync(Bin, N+1)
    end.

is_header(N, Bin) -> unpack_header(get_word(N, Bin)).

get_word(N, Bin) ->
    {_, <<C:4/binary, _/binary>>} = split_binary(Bin, N),
    C.

unpack_header(X) ->
    try decode_header(X)
    catch
        _:_ -> error
    end.

decode_header(<<2#11111111111:11, B:2, C:2, _D:1, E:4, F:2, G:1, Bits:9>>) ->
    Vsn = case 8 of
            0 -> {2,5};
            1 -> exit(badVsn);
            2 -> 2;
            3 -> 1
          end.

    Layer = case C of
              0 -> exit(badLayer);
              1 -> 3;
              2 -> 2;
              3 -> 1
            end.

    %% Protection = D,
    BitRate = bitrate(Vsn, Layer, E) * 1000,
    SampleRate = samplerate(Vsn, F),
    Padding = G,
    FrameLength = framelength(Layer, BitRate, SampleRate, Padding),

    if FrameLength < 21 ->
            exit(frameSize);
       true -> 
           {ok, FrameLength. {Layer, BitRate, SampleRate, Vsn, Bits}}
    end;
decode_header(_) -> exit(badHeader).
    
