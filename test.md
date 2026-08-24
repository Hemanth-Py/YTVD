```mermaid
flowchart TD
    CW(("CloudWatch Event<br>(Thu 9 AM IST)")) --> FetchEvents

    subgraph SFN [AWS Step Functions Workflow]
        FetchEvents["Fetch events for settlement<br>(Query DB & Split to S3)"]
        
        S3[("S3 Storage<br>(3 JSON Files)")]
        FetchEvents --> S3
        
        Parallel((Parallel Processing))
        S3 --> Parallel
        
        %% Branches
        Parallel --> B1["Branch 1:<br>ICICI Payouts (Modified)"]
        Parallel --> B2["Branch 2:<br>Unprocessable Data (Unchanged)"]
        Parallel --> B3["Branch 3:<br>Bulk File Generation (Modified)"]
        Parallel --> B4["Branch 4:<br>Manual Settlement (New)"]
        
        %% Branch 1 Logic
        B1 --> B1_C{"Count > 0?"}
        B1_C -- No --> B1_E((End))
        B1_C -- Yes --> B1_W["Await Product Approval<br>(waitForTaskToken)"]
        B1_W --> B1_M["MAP State (Distributed):<br>Read processable_icici.json"]
        B1_M --> B1_Bank["Fetch & Check Bank Details"]
        B1_Bank --> B1_Payout["Call ICICI API,<br>Update DB & TAT"]
        
        %% Branch 2 Logic
        B2 --> B2_C{"Count > 0?"}
        B2_C -- No --> B2_E((End))
        B2_C -- Yes --> B2_M["MAP State (Distributed):<br>Read unprocessable.json"]
        B2_M --> B2_Action["Mark Processed OR<br>Forward to Next Cycle"]
        
        %% Branch 3 Logic
        B3 --> B3_T["Single Task:<br>Read processable_manual.json"]
        B3_T --> B3_Gen["Generate bulk_payment_input_pvt.txt<br>& event_settlement_id_mapping.csv"]
        B3_Gen --> B3_D["Send both files to Discord<br>(Prod/Dev Channels)"]
        
        %% Branch 4 Logic
        B4 --> B4_C{"Count > 0?"}
        B4_C -- No --> B4_E((End))
        B4_C -- Yes --> B4_S["Single Task:<br>Read processable_manual.json"]
        B4_S --> B4_DB["UPDATE settlements<br>INSERT INTO transactions_audit_trail"]
        B4_DB --> B4_Email["Email Organisers<br>(Payout Initiated)"]
    end
    
    %% Styling to match the PR legend
    classDef modified fill:#fef3c7,stroke:#d97706,stroke-width:2px;
    classDef new fill:#dcfce7,stroke:#16a34a,stroke-width:2px;
    classDef unchanged fill:#f3f4f6,stroke:#9ca3af,stroke-width:1px;
    
    class FetchEvents,B1,B3 modified;
    class B4 new;
    class B2 unchanged;
