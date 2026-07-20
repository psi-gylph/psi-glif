# ψ-GLIF Repository Architecture
Version: 0.1
Status: Active
Scope: Public Repository

---

# Purpose

The ψ-GLIF repository is the public publication and provenance layer of the ψ-GLIF ecosystem.

It is **not** the private development environment.

It is **not** the production environment.

It is **not** the research laboratory.

It is the controlled public interface through which approved works, documentation, provenance records, and archival software are published.

---

# Core Philosophy

The repository is designed around one principle:

> Nothing enters the public archive automatically.

Every artifact is intentionally reviewed before publication.

Human review always precedes publication.

---

# Repository Role

The repository serves five primary purposes.

## 1. Public Publication

Maintain public records of published ψ-GLIF works.

Examples include:

- published collections
- published items
- publication manifests
- collector documentation
- provenance records

---

## 2. Provenance

Maintain verifiable history for public artifacts.

The repository records:

- publication history
- checksums
- version history
- authorship
- publication relationships

It does not reconstruct unpublished history.

---

## 3. Intellectual Property

Provide documentation that supports intellectual property management.

Examples include:

- invention records
- concept disclosures
- prior art research
- patent preparation
- publication chronology

The repository itself does not claim legal protection.

---

## 4. Smart Archive

The repository contains software whose purpose is to maintain the archive itself.

Examples include:

- metadata validation
- checksum verification
- duplicate detection
- broken link detection
- archive consistency checks

These tools operate only on repository contents.

---

## 5. Agent Development

Public archive agents may be developed inside this repository.

Their responsibility is limited to:

- archive review
- validation
- reporting
- consistency analysis

Agents must never operate on private systems.

---

# Repository Boundaries

The repository intentionally excludes private development.

Private work remains outside the repository.

The repository never becomes a mirror of the development environment.

---

# PSI-LAB Relationship

PSI-LAB is an independent private development environment.

This repository references PSI-LAB only as an external system.

The repository never contains:

- PSI-LAB source code
- PSI-LAB runtime
- PSI-LAB internal paths
- PSI-LAB databases
- PSI-LAB unpublished experiments
- PSI-LAB local architecture
- PSI-LAB automation

Any artifact originating from PSI-LAB requires explicit human approval before publication.

---

# Publication Flow

Private creation

↓

Human review

↓

Approval

↓

Public repository

↓

Public distribution

No automatic synchronization exists.

---

# Import Policy

Default state:

PRIVATE

Every artifact is considered private until approved.

Repository inclusion requires:

1. Human selection
2. Content review
3. Security review
4. Provenance review
5. Publication approval

Only then may the artifact enter the repository.

---

# Security Principles

The repository must never contain:

- API keys
- secrets
- wallet information
- private credentials
- seed phrases
- private blockchain infrastructure
- unpublished economic systems
- unpublished research

Unknown information remains null.

Assumptions are never recorded as facts.

---

# Economic Separation

The repository is not an economic platform.

It does not contain:

- token economy
- smart contracts under development
- wallet infrastructure
- pricing logic
- financial automation

Public publication records may reference already published assets only.

---

# Design Principles

The repository values:

- clarity
- traceability
- provenance
- reproducibility
- intentional publication
- human accountability

Automation supports these principles but never replaces human approval.

---

# Long-Term Vision

The repository should evolve into a self-maintaining public archive.

Future software may assist in:

- validation
- integrity checking
- publication review
- metadata consistency
- provenance verification

The repository remains intentionally separated from private creation environments.

---

# Guiding Principle

Private creation remains private.

Public publication remains intentional.

The repository exists to preserve what has been deliberately shared—not to expose what has not.
