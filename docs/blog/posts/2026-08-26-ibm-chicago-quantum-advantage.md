---
title: "IBM and the University of Chicago Show Quantum Advantage — With Proof"
date: 2026-08-26T05:16:41+00:00
author:
  - eelco
categories:
  - Technology
  - Science
  - Quantum Computing
  - Research
  - Innovation
tags:
  - IBM
  - Quantum Computing
  - University of Chicago
  - Quantum Advantage
  - Error Correction
  - Logical Qubits
---
On July 30, 2026, IBM and researchers from the University of Chicago announced a quantum computation that meets the fundamental criteria for quantum advantage: a task beyond the practical reach of the best known classical methods, completed in about fifteen minutes. Just as important, the team found a way to verify how reliable the result actually was — addressing the long-standing problem that has made quantum advantage claims so hard to trust.

<!-- more -->

### 70 Logical Qubits and a Hard Sampling Problem

In their paper "Sampling hard circuits with verifiably high fidelity," the researchers used a new error correction method to encode 70 logical qubits — quantum bits shielded from noise by spreading them across multiple physical qubits. The team executed 2,415 logical two-qubit operations and 468 logical "T gates," both measures of circuit complexity, making it one of the largest demonstrations of logical quantum computing to date.

Crucially, the encoding worked: the effective logical error rate came out ten times lower than the physical error rate, keeping the circuit's fidelity remarkably high despite the large number of operations. That error suppression is what made a long, complex computation possible at all.

### Why Verification Matters

For years, researchers have benchmarked quantum computers with random circuit sampling (RCS): ask the machine to produce patterns so complex that a classical computer cannot efficiently reproduce them. The catch has always been verification — the harder the problem, the harder it is to prove the quantum computer's answer is correct without making strong assumptions about the machine's inner workings.

The team's solution is a structured alternative to RCS. They proved it retains the same computational hardness as RCS, but the added structure lets the experiment detect errors while the computation runs. "Verification remains one of the biggest challenges in firmly establishing experimental quantum advantage," said Bill Fefferman, associate professor at the University of Chicago. "This experiment develops techniques to better characterize the fidelity of hard quantum states under noise, increasing confidence that the quantum computer is solving a computationally hard problem."

### Fifteen Minutes vs. Infeasible

The IBM quantum computer finished the task in approximately 15 minutes. The researchers showed that many leading classical simulation approaches would face runtimes too long to be practical. The circuits and results have been openly released on IBM's Quantum Advantage Tracker, so others can examine and build on the work.

"This is now firmly the quantum advantage era," said Jay Gambetta, Director of IBM Research. "We have demonstrated a quantum computation beyond the practical reach of classical computers that establishes, with statistical confidence, a lower bound on how faithfully it was executed."

### What It Means

Reliable error correction and confidence in the output are prerequisites for scaling quantum computers to problems that matter commercially. The UChicago team notes that better verification could unlock practical applications for the next generation of machines. As with all quantum advantage claims, independent scrutiny will follow — but combining a classically intractable computation with a verifiable result is a significant step toward making quantum computers trustworthy tools rather than laboratory curiosities. IBM announced this result alongside two further quantum advantage demonstrations with ecosystem partners on the same day.

### Sources

- [IBM Newsroom: IBM and The University of Chicago Demonstrate Quantum Advantage, Establishing Trusted Quantum Computation on Logical Circuits](https://newsroom.ibm.com/2026-07-30-ibm-and-the-university-of-chicago-demonstrate-quantum-advantage,-establishing-trusted-quantum-computation-on-logical-circuits)
- [UChicago News: IBM, UChicago demonstrate 'quantum advantage'](https://news.uchicago.edu/story/ibm-uchicago-demonstrate-quantum-advantage-outperforming-traditional-computers-quantum)
- [SciTechDaily: Quantum Computer Solves a Problem in 15 Minutes That Classical Methods Can't Practically Compute](https://scitechdaily.com/quantum-computer-solves-a-problem-in-15-minutes-that-classical-methods-cant-practically-compute/)
- [arXiv: Sampling hard circuits with verifiably high fidelity (DOI 2607.25941)](https://arxiv.org/abs/2607.25941)
- [IBM Quantum Advantage Tracker](https://www.ibm.com/quantum/blog/quantum-advantage)
