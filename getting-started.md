<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <title>Getting Started with AgDR v0.2 | Accountability.ai</title>
    <style>
        /* Reset & Base Styles - Clean, no overlapping issues */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;
            line-height: 1.6;
            color: #1a1a1a;
            background: #ffffff;
            scroll-behavior: smooth;
        }

        /* Typography */
        h1, h2, h3 {
            font-weight: 600;
            line-height: 1.25;
            margin-top: 2rem;
            margin-bottom: 1rem;
            color: #0a0a0a;
        }

        h1 {
            font-size: 2.5rem;
            margin-top: 0;
            border-bottom: 2px solid #eaeef2;
            padding-bottom: 0.75rem;
        }

        h2 {
            font-size: 1.75rem;
            border-left: 4px solid #0066cc;
            padding-left: 1rem;
        }

        h3 {
            font-size: 1.35rem;
            color: #2c3e50;
        }

        p {
            margin-bottom: 1.25rem;
            color: #2c3e50;
        }

        a {
            color: #0066cc;
            text-decoration: none;
            border-bottom: 1px solid transparent;
            transition: border-color 0.2s ease;
        }

        a:hover {
            border-bottom-color: #0066cc;
        }

        /* Layout - No overlapping containers */
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem 1.5rem;
        }

        /* Header / Navigation */
        .site-header {
            background: #f8fafc;
            border-bottom: 1px solid #e2e8f0;
            position: relative; /* Not fixed/absolute to avoid overlay */
            width: 100%;
        }

        .nav {
            max-width: 1200px;
            margin: 0 auto;
            padding: 1rem 1.5rem;
            display: flex;
            gap: 2rem;
            flex-wrap: wrap;
        }

        .nav a {
            font-weight: 500;
            border-bottom: none;
        }

        /* Code blocks - Critical for preventing overflow/overlay */
        pre {
            background: #1e293b;
            color: #e2e8f0;
            padding: 1.25rem;
            border-radius: 8px;
            overflow-x: auto;
            overflow-y: hidden;
            white-space: pre-wrap;
            word-wrap: break-word;
            font-family: 'SF Mono', 'Menlo', 'Courier New', monospace;
            font-size: 0.9rem;
            line-height: 1.5;
            margin: 1.5rem 0;
            border: 1px solid #334155;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        }

        code {
            font-family: 'SF Mono', 'Menlo', 'Courier New', monospace;
            background: #f1f5f9;
            padding: 0.2rem 0.4rem;
            border-radius: 4px;
            font-size: 0.875em;
            color: #0f172a;
        }

        pre code {
            background: transparent;
            padding: 0;
            color: inherit;
        }

        /* Tables - Clean and responsive */
        .table-wrapper {
            overflow-x: auto;
            margin: 1.5rem 0;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.95rem;
        }

        th, td {
            padding: 0.75rem 1rem;
            text-align: left;
            border-bottom: 1px solid #e2e8f0;
        }

        th {
            background: #f8fafc;
            font-weight: 600;
            color: #0f172a;
        }

        tr:last-child td {
            border-bottom: none;
        }

        /* Cards / Sections */
        .card {
            background: #f8fafc;
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1.5rem 0;
            border: 1px solid #e2e8f0;
            box-shadow: 0 1px 2px rgba(0,0,0,0.03);
        }

        .card h3 {
            margin-top: 0;
        }

        /* Footer */
        .site-footer {
            margin-top: 3rem;
            padding: 2rem 1.5rem;
            background: #f8fafc;
            border-top: 1px solid #e2e8f0;
            text-align: center;
            font-size: 0.875rem;
            color: #5a6874;
        }

        /* Responsive */
        @media (max-width: 768px) {
            .container {
                padding: 1.5rem;
            }
            
            h1 {
                font-size: 2rem;
            }
            
            h2 {
                font-size: 1.5rem;
            }
            
            .nav {
                gap: 1rem;
                flex-direction: column;
                align-items: flex-start;
            }
            
            pre {
                font-size: 0.8rem;
                padding: 1rem;
            }
        }

        /* Utility - No z-index wars */
        .no-overflow {
            overflow: visible;
        }

        /* Highlight for important elements */
        .highlight {
            background: #fef9e3;
            border-left: 4px solid #f5b042;
            padding: 1rem;
            margin: 1.5rem 0;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <header class="site-header">
        <div class="nav">
            <a href="/">🏛️ Accountability.ai</a>
            <a href="/getting-started.html">Getting Started</a>
            <a href="/ppp-pillars.html">PPP Pillars</a>
            <a href="/spec.html">Spec</a>
            <a href="https://github.com/accountability-source/AgDR">GitHub</a>
        </div>
    </header>

    <main class="container">
        <h1>Getting Started with AgDR v0.2</h1>
        
        <p class="lead" style="font-size: 1.2rem; color: #2c3e50; margin-bottom: 2rem;">
            Welcome to the <strong>Atomic Genesis Decision Record Standard</strong>. 
            AgDR gives every autonomous agent decision a tamper-evident, cryptographically signed record 
            that is admissible in court today — and in 2076.
        </p>

        <div class="highlight">
            <strong>⚡ Core Guarantee:</strong> Every inference is captured atomically, signed with BLAKE3, 
            and persisted to a tamper-evident Merkle-append log. No edits. No backdating.
        </div>

        <h2>1. Download the Spec</h2>
        <p>Start by downloading the canonical specification. This defines the exact structure of an AgDR record.</p>
        
        <pre><code>curl -O https://raw.githubusercontent.com/accountability-source/AgDR/main/specs/agdr-v0.2.json</code></pre>
        
        <p>Read it. Understand the core guarantee before writing any code. The atomic capture ensures:</p>
        
        <div class="table-wrapper">
            <table>
                <thead>
                    <tr>
                        <th>Component</th>
                        <th>Description</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><code>sign(BLAKE3(...))</code></td>
                        <td>Cryptographic signature over the inference payload</td>
                    </tr>
                    <tr>
                        <td><code>persist(Merkle-append)</code></td>
                        <td>Immutable append-only log with Merkle tree verification</td>
                    </tr>
                    <tr>
                        <td><code>return c(...)</code></td>
                        <td>Returns the capture certificate for audit</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <h2>2. Install the Python SDK</h2>
        <p>Use the official Python package to integrate AgDR into your agent workflows.</p>
        
        <pre><code>pip install agdr-aki</code></pre>
        
        <p>Or install directly from source to get the latest development features:</p>
        
        <pre><code>git clone https://github.com/accountability-source/AgDR.git
cd AgDR/python-sdk
pip install -e .</code></pre>

        <h2>3. Initialize Your First Capture</h2>
        <p>Create a simple capture to understand the flow. The SDK handles signing and persistence automatically.</p>
        
        <pre><code>from agdr import AtomicKernelInference

# Initialize with your fiduciary key
aki = AtomicKernelInference(
    agent_id="agent-001",
    private_key_path="path/to/your/private_key.pem"
)

# Capture an inference atomically
capture = aki.capture(
    provenance="Current context: user requested financial analysis",
    place="Target: generate compliant investment report",
    purpose="Reason: fiduciary duty to provide accurate, lawful advice",
    payload={
        "model": "gpt-4",
        "temperature": 0.7,
        "prompt": "Analyze market trends..."
    }
)

# The capture certificate is now signed and persisted
print(f"Capture ID: {capture.id}")
print(f"Signature: {capture.signature.hex()}")
print(f"Merkle Root: {capture.merkle_root}")</code></pre>

        <div class="card">
            <h3>📋 What Just Happened?</h3>
            <p>The <code>capture()</code> method performed an atomic transaction:</p>
            <ul style="margin-left: 1.5rem; margin-top: 0.5rem;">
                <li>✅ Hashed the entire inference payload with BLAKE3</li>
                <li>✅ Digitally signed the hash with your private key</li>
                <li>✅ Appended the record to a tamper-evident Merkle log</li>
                <li>✅ Returned a verifiable capture certificate</li>
            </ul>
            <p style="margin-top: 0.75rem;">All three PPP pillars (Provenance, Place, Purpose) are captured <strong>atomically</strong> — no race conditions, no edits.</p>
        </div>

        <h2>4. Verify a Capture</h2>
        <p>Any third party can independently verify the authenticity and integrity of a capture.</p>
        
        <pre><code>from agdr import Verifier

verifier = Verifier()
result = verifier.verify(capture_id="capture-abc123")

if result.valid:
    print("✓ Signature valid")
    print("✓ Merkle proof verified")
    print("✓ No tampering detected")
else:
    print("✗ Capture invalid or compromised")</code></pre>

        <h2>5. Integrate with Your Agent Framework</h2>
        <p>Wrap your agent's decision points with AgDR captures to create an immutable audit trail.</p>
        
        <pre><code>class CompliantAgent:
    def __init__(self, aki):
        self.aki = aki
    
    def decide(self, input_data):
        # Capture the inference before execution
        capture = self.aki.capture(
            provenance=f"State: {self.get_state()}",
            place="Goal: make optimal decision",
            purpose="Alignment: maximize user benefit",
            payload=input_data
        )
        
        # Execute the decision
        result = self._execute(input_data)
        
        # Attach capture ID to result for traceability
        result.capture_id = capture.id
        return result</code></pre>

        <h2>Next Steps</h2>
        <div style="display: flex; gap: 1rem; flex-wrap: wrap; margin: 2rem 0;">
            <a href="/ppp-pillars.html" style="background: #0066cc; color: white; padding: 0.75rem 1.5rem; border-radius: 6px; border-bottom: none;">📖 Read PPP Pillars →</a>
            <a href="https://github.com/accountability-source/AgDR" style="background: #f1f5f9; color: #1e293b; padding: 0.75rem 1.5rem; border-radius: 6px; border-bottom: none;">💻 View on GitHub</a>
            <a href="/spec.html" style="background: #f1f5f9; color: #1e293b; padding: 0.75rem 1.5rem; border-radius: 6px; border-bottom: none;">📄 Full Specification</a>
        </div>

        <div class="highlight" style="background: #e6f7e6; border-left-color: #2c8c2c;">
            <strong>🔒 Legal Admissibility:</strong> AgDR records are designed to meet evidentiary standards globally. 
            The combination of cryptographic signatures, Merkle proofs, and atomic PPP capture creates a 
            contemporaneous record that courts have already accepted in pilot jurisdictions.
        </div>
    </main>

    <footer class="site-footer">
        <p>AgDR v0.2 — Atomic Kernel Inference Standard</p>
        <p style="margin-top: 0.5rem;">
            <a href="https://github.com/accountability-source/AgDR">Canonical Source</a> • 
            <a href="/license.html">MIT License</a> • 
            <a href="/contact.html">Contact</a>
        </p>
    </footer>
</body>
</html>
