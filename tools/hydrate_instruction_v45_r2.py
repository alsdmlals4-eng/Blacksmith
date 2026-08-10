#!/usr/bin/env python3
from __future__ import annotations

import base64
import gzip
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAYLOAD_DIR = ROOT / "tools/.instruction_v45_r2_payload"
OUT = ROOT / "PROJECT_TOTAL_PLANNING_IMPLEMENTATION_AND_DELIVERY_INSTRUCTION.md"

EXPECTED_PART_HASHES = [
    "8b21f4a1bc8ca70ccb1fc59a6bb966ab5d218f0a4d51afea1ee4d82ca30f7ff8",
    "2042029d8febc03f43e135145fe8773489ee718c65b5b74260d26e3a43d29285",
    "b763c565f5f0726624bde138d49989816a39f695aa38089adc682ac7b7f99cf0",
    "351b98e511a656080aa188eff6dfece6fc89ae8bf31ee6b8cd77d37ae455ae20",
    "71529489ff39e765dcd636ae2d75f9b3a971b16706fbd3bac90ef939c827c95c",
    "06cc408cef7749197556c8f3099615bf696cc89bb7a77a672b1dc59743ec98ad",
    "b85056e08d9fdc6127544f858cd4e284933e9b72b591b40c428ad657af8e97d1",
    "c14d04b137e3d6e3a7572aa51e879cc5aa1cb4be351db9de9335529bfa6f5e4b",
    "3c2beeb6cb83e5e07e979e3929bab2c90dee57efe35c14650f807ecb9a968950",
    "1890abc1c9587b9f071177f7b01faf1cffacb8fef39ea54f0f4b4eaaf467c03d",
    "adb3e63b2693fceecc80f1420bb86dbe1446389f61f7d72beca484964def87f3",
    "31e43b4dff3a395776e1cdfb3157d4061aa7ee2bd809772eebbbf02d8d891dc6",
    "6e30662c0306ec5fe183cee801998877fc60e2e17a0150bc6d7ef0926c8d88e3",
    "74ed09124adcf9afe2e9219b92c601f18050845fa808a8aa191c57a9e68a3d16",
    "bc1c9be781fc2ec05eb92855326a0a8dab9c1367f805a6266cfa8720dccc8c27",
    "b5346eca1e6d3ed07d64696ac571e55f2218e5626d9a4bfe31383bba353d175c",
    "3f73b74198b8021b22a8cec5894cb3ce83595f1711bd42951fe565a3acc5e071",
    "6c6938bac977c43424a79de8f36d1832beebe8099d990139c5c9ecc1add2e925",
    "bacb7f097666be8596c75dcb1afd54ce4e9a7c5d30d504d89b53b3cac734cf20",
    "8e340adeac8929499d7c383560051f6c44a26cbf715f5ad1e619acaff3dd8a2d",
    "6d5cc327fbd8101a3453465c83f0596b06506f866d877391b6c005ae0313ae46",
    "91f71c8d3e9ced9a280a7eae44b83ba03a20f9b53a498f620995483509920814",
    "a7627cbb2d353fc3395e5302c121373107f009b3c5232d8484e5468c95801e93",
    "c32ace699f558fed4aba8a8d5dad48d8610b023028494cd7428f4f8a8ea23ea7",
    "701b2f1e034452d83daa0d74320c09d1579820d453e0aeeafb67afd45991e984",
    "20cc5c9cbad8641ae0472bb9fb9807db1fb6e55116332a9a95c1f94b98c5aa84",
    "37eca5ec2d40bfb978b329a88576ced905d81207ac5e1d18557134c108e6ab90",
    "94fcbb04adb8c174c8188d9fa96a5bc2385609cc262fc12dd24d7395f858147f",
    "af263884767aca0fcfce319ee33b53772c804748e872f829d504e6962d13e5b5",
    "058883afbee1208694b62fb7e36aee6de677429503efba3da1a5330573237ef6",
    "3de90438df626ab9db894b4dbf822e8e1c7a91ba73597a14644cfaa66f7e2e25",
    "32e864a273939f89383c0f8178df8941631b06896a25397af8c153d9c1240aca",
    "c106540bb54962385794d0fc4523998104a1d9899a5091fc668e41c50938cc23",
    "1afea580ee871bdc2c21d225a0a776f1603bf9b6893cfd4290840c532a27ff29",
    "09e53d62b40f107cc446488d04ee075e133570e5ddd9de327ab8b479f1158c57",
    "9fab634a8839fd202de001c1a501c264eb98a8996dcb7ab5b55f74fd892a9783",
    "d8ea5e87c9310f756a3799f99076b36d79d66c64c40b302f292dcae432bd4127",
    "2826762f64ee2ccf99a487a4e5ee494ec32d2e3e515dbd1b7dca60d3e55bfe7c",
    "a8abaadd915e107ed6cacb5384418dc21011b4c9cceeed707d58898e93f15c24",
    "ae21c35637f4fe0bf2c26aaef0af86cf755ee1654a7daeb551e0ef3b09f1a95a",
]
EXPECTED_GZIP_SHA256 = "f8c7594e72cd55a84e04dbb2bcb39e4f597f691027f9a267e3d5f6d2bc7ce297"
EXPECTED_GZIP_BYTES = 29318
EXPECTED_B64_CHARS = 39092
EXPECTED_RAW_SHA256 = "3f898b7e2749a2e1900e9df48183f02d4fbc735fd0e80297f28bb09317144de4"
EXPECTED_RAW_BYTES = 77734


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    parts: list[str] = []
    for index, expected_hash in enumerate(EXPECTED_PART_HASHES):
        path = PAYLOAD_DIR / f"p{index:03d}.b64"
        if not path.is_file():
            raise SystemExit(f"missing payload part: {path}")
        text = path.read_text(encoding="ascii")
        expected_len = 92 if index == 39 else 1000
        if len(text) != expected_len:
            raise SystemExit(f"part {index:03d} length mismatch: {len(text)} != {expected_len}")
        actual_hash = sha256(text.encode("ascii"))
        if actual_hash != expected_hash:
            raise SystemExit(f"part {index:03d} sha256 mismatch: {actual_hash} != {expected_hash}")
        parts.append(text)

    encoded = "".join(parts)
    if len(encoded) != EXPECTED_B64_CHARS:
        raise SystemExit(f"base64 length mismatch: {len(encoded)} != {EXPECTED_B64_CHARS}")

    compressed = base64.b64decode(encoded, validate=True)
    if len(compressed) != EXPECTED_GZIP_BYTES:
        raise SystemExit(f"gzip length mismatch: {len(compressed)} != {EXPECTED_GZIP_BYTES}")
    compressed_hash = sha256(compressed)
    if compressed_hash != EXPECTED_GZIP_SHA256:
        raise SystemExit(f"gzip sha256 mismatch: {compressed_hash} != {EXPECTED_GZIP_SHA256}")

    raw = gzip.decompress(compressed)
    if len(raw) != EXPECTED_RAW_BYTES:
        raise SystemExit(f"raw length mismatch: {len(raw)} != {EXPECTED_RAW_BYTES}")
    raw_hash = sha256(raw)
    if raw_hash != EXPECTED_RAW_SHA256:
        raise SystemExit(f"raw sha256 mismatch: {raw_hash} != {EXPECTED_RAW_SHA256}")

    text = raw.decode("utf-8")
    for token in (
        "contract_name: PROJECT_TOTAL_PLANNING_IMPLEMENTATION_AND_DELIVERY_INSTRUCTION",
        "contract_version: '4.5'",
        "revision: '2026-08-11-r2'",
        "execution_scope_guard: INSTRUCTION_DOCUMENT_UPDATE_ONLY_UNLESS_EXPLICIT_FUTURE_EXECUTION_REQUEST",
        "current_conversation_merge_policy: RECOMMENDED_AUTO_APPROVAL_WITHIN_ALREADY_APPROVED_SCOPE",
        "Switchy-Express-Cargo-Puzzle",
    ):
        if token not in text:
            raise SystemExit(f"required source token missing: {token}")

    OUT.write_bytes(raw)
    print(f"HYDRATED {OUT.name}")
    print(f"RAW_BYTES={len(raw)}")
    print(f"RAW_SHA256={raw_hash}")
    print(f"GZIP_BYTES={len(compressed)}")
    print(f"GZIP_SHA256={compressed_hash}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
