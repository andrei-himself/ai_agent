# ai_agent

A small, toy agent that analyzes a codebase and proposes fixes/refactors using an LLM. It reads files from a workspace, suggests changes, and can write updates when explicitly allowed.

Security Heads-Up

This is a toy project. No guarantees of safety or correctness.
By default, keep runs in a restricted workspace and require confirmation before writes. Review settings before use.
Do not point it at sensitive directories or give it access to credentials.
Logs and prompts may contain snippets of your code—treat outputs as potentially sensitive.
If you open a PR or issue, don’t include secrets or proprietary code.