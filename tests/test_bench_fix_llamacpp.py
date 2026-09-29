"""scripts/bench_fix_llamacpp.py: output-token counts come from the server,
count-dependent metrics are recomputed with the client's formulas, and a
run with a failed request or a short server count is refused."""
import importlib.util
import pathlib

import pytest

_MOD_PATH = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "bench_fix_llamacpp.py"
_spec = importlib.util.spec_from_file_location("bench_fix_llamacpp", _MOD_PATH)
bf = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bf)

L = 4  # output tokens per request


def _result(**kw):
    # two requests: TTFT 1 s / 2 s, three ITLs each summing to 0.3 s / 0.6 s
    d = {"num_prompts": 2, "completed": 2, "duration": 10.0, "total_input_tokens": 100,
         "total_output_tokens": 7, "output_throughput": 0.7, "total_token_throughput": 10.7,
         "mean_tpot_ms": 1.0, "median_tpot_ms": 1.0, "std_tpot_ms": 0.0,
         "p50_tpot_ms": 1.0, "p90_tpot_ms": 1.0, "p99_tpot_ms": 1.0,
         "mean_e2el_ms": 1950.0, "mean_ttft_ms": 1500.0,
         "input_lens": [50, 50], "output_lens": [4, 3], "ttfts": [1.0, 2.0],
         "itls": [[0.1, 0.1, 0.1], [0.2, 0.2, 0.2]], "generated_texts": ["a", "b"],
         "errors": ["", ""]}
    d.update(kw)
    return d


def test_counts_and_tpot_recomputed():
    out = bf.fix(_result(), L, L * 3, 99)
    assert out["total_output_tokens"] == 8
    assert out["output_throughput"] == pytest.approx(0.8)
    assert out["total_token_throughput"] == pytest.approx(10.8)
    assert out["mean_tpot_ms"] == pytest.approx(150.0)  # (100 + 200) / 2 ms
    assert out["p50_tpot_ms"] == pytest.approx(150.0)
    assert out["p99_tpot_ms"] == pytest.approx(199.0)
    assert out["std_tpot_ms"] == pytest.approx(50.0)
    assert out["client_retokenized"]["total_output_tokens"] == 7
    assert out["mean_ttft_ms"] == 1500.0 and out["mean_e2el_ms"] == 1950.0
    assert out["request_decode_s"] == pytest.approx([0.3, 0.6])
    assert "itls" not in out and "generated_texts" not in out
    assert out["llamacpp_tokens_predicted"] == 12 and out["llamacpp_prompt_tokens_processed"] == 99


def test_failed_request_refused_with_error_text():
    d = _result(completed=1, errors=["", "Never received a valid chunk"])
    with pytest.raises(ValueError, match="completed 1 of 2.*Never received a valid chunk"):
        bf.fix(d, L, L * 3, 0)


# the 2026-09-29 traceback, abridged
LOSS = ('Traceback ...\n  File "aiohttp/client.py", line 748, in _connect_and_send_request\n'
        '    await resp.start(conn)\n'
        '  File "aiohttp/client_reqrep.py", line 532, in start\n'
        '    message, payload = await protocol.read()\n'
        'aiohttp.client_exceptions.ServerDisconnectedError: Server disconnected\n')


def _with_loss(n_ok=99):
    """n_ok requests like the first of _result, plus one transport loss."""
    n = n_ok + 1
    return _result(num_prompts=n, completed=n_ok, mean_e2el_ms=1300.0,
                   ttfts=[1.0] * n_ok + [0.0], itls=[[0.1, 0.1, 0.1]] * n_ok + [[]],
                   errors=[""] * n_ok + [LOSS])


def test_transport_loss_accepted_and_recorded():
    out = bf.fix(_with_loss(), L, L * 100, 0)
    assert out["lost_requests"] == [99]
    assert out["total_output_tokens"] == 4 * 99
    assert out["mean_tpot_ms"] == pytest.approx(100.0)
    assert len(out["request_ttfts_s"]) == 99


def _losses(n, lost):
    ok = n - lost
    return _result(num_prompts=n, completed=ok, mean_e2el_ms=1300.0,
                   ttfts=[1.0] * ok + [0.0] * lost,
                   itls=[[0.1, 0.1, 0.1]] * ok + [[]] * lost,
                   errors=[""] * ok + [LOSS] * lost)


def test_transport_losses_up_to_one_percent_accepted():
    out = bf.fix(_losses(200, 2), L, L * 199, 0)
    assert out["lost_requests"] == [198, 199]


def test_transport_losses_over_one_percent_refused():
    # the 2026-09-29 Q8_0 concurrency-8 run: 3 of 200 lost
    with pytest.raises(ValueError, match=r"lost 3 of 200 requests .*\(limit 1%\)"):
        bf.fix(_losses(200, 3), L, L * 198, 0)


def test_one_loss_allowed_in_a_small_cell():
    assert bf.fix(_losses(32, 1), L, L * 32, 0)["lost_requests"] == [31]
    # the Q4_K_M sweep's concurrency-2 cell: 4 of 32 lost
    with pytest.raises(ValueError, match=r"lost 4 of 32 requests"):
        bf.fix(_losses(32, 4), L, L * 29, 0)


def test_lost_request_must_not_have_generated():
    with pytest.raises(ValueError, match=r"want 4 x \(99 \+ 1\)"):
        bf.fix(_with_loss(), L, L * 101, 0)


def test_other_error_refused_even_when_single():
    d = _with_loss()
    d["errors"][-1] = "aiohttp.client_exceptions.ClientPayloadError: mid-stream"
    with pytest.raises(ValueError, match="completed 99 of 100.*ClientPayloadError"):
        bf.fix(d, L, L * 100, 0)


def test_short_server_count_refused():
    with pytest.raises(ValueError, match=r"server generated 11 tokens, want 4 x \(2 \+ 1\)"):
        bf.fix(_result(), L, 11, 0)


def test_detail_must_reproduce_client_e2e():
    with pytest.raises(ValueError, match="do not reproduce"):
        bf.fix(_result(mean_e2el_ms=2500.0), L, L * 3, 0)


def test_percentile_matches_numpy_linear():
    assert bf.percentile([1, 2, 3, 4], 90) == pytest.approx(3.7)
    assert bf.percentile([5], 99) == 5
