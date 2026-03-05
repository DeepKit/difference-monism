$vols = @(
@{V="01";T="The Cost of Living";C="Insurance Loophole";A="NPC (Brad)";S="v1.0: Red Lines + Human Check (Baseline)";E="104_C First Appearance";O="Victory (Costly)";F="Traditional"},
@{V="02";T="The Loss in Transit";C="Logistics Chain";A="NPC + Chain";S="v1.1: Minimum Accountability";E="Ghost Cargo";O="Bitter Victory";F="Email Chain Collage"},
@{V="03";T="The Tyranny of Distance";C="Resource Scarcity";A="Faceless Algorithm";S="v1.2: Delay is Harm";E="System Age: 15 Years";O="Stalemate";F="Time Jump"},
@{V="04";T="The Hunger Line";C="Compliance Trap";A="Law";S="v1.3: Outsourcing Liability";E="Outsourcing Contracts";O="Failure";F="SOP/Training Materials"},
@{V="05";T="The Fiction of Identity";C="Irreversible Harm";A="Adaptive (Learning)";S="v1.4: Identity is Privacy";E="104_C Identity Data";O="Reversal";F="Traditional"},
@{V="06";T="The Surplus of Labor";C="Loophole";A="NPC + Union";S="v1.5: Labor Time Rights";E="Surplus Value Flow";O="Victory (Temporary)";F="Hearing Transcript"},
@{V="07";T="The Boundary of Punishment";C="Responsibility Chain";A="Chain (Prison)";S="v1.6: Penalty Chain Clarity";E="Rules Origin";O="Stalemate";F="Court Record"},
@{V="08";T="The Politics of Water";C="Resource Scarcity";A="Faceless + Law";S="v1.7: Allocation Priority";E="Infrastructure Control";O="Failure";F="Engineering Report"},
@{V="09";T="The Quarantine";C="Compliance Trap";A="Adaptive (Evolution)";S="v1.8: Health vs Liberty";E="Isolation Algorithm";O="Bitter Victory";F="Pandemic Data Table"},
@{V="10";T="The Logistics of War";C="Irreversible Harm";A="Chain + Adaptive";S="v1.9: War Cost Allocation";E="104_C Military Use";O="Reversal (Ethan Dies)";F="Logistics Log"},
@{V="11";T="The Silver Lie";C="Resource Scarcity";A="Faceless (Finance)";S="v2.0: Symbol World Start";E="Finance Links to 104_C";O="Victory";F="Trading Log"},
@{V="12";T="The Collapse of Credit";C="Loophole";A="Narrative (PR)";S="v2.1: Credit is Rule";E="Bankruptcy Chain";O="Failure (Upgrade)";F="News Summary"},
@{V="13";T="The Trap of Contract";C="Compliance Trap";A="Law + Narrative";S="v2.2: Unfair Terms Violence";E="Universal Terms Template";O="Stalemate";F="Contract Collage"},
@{V="14";T="The Economics of Addiction";C="Responsibility Chain";A="Adaptive";S="v2.3: Addiction is Design";E="Rec Algo Origin";O="Reversal";F="User Data Screenshot"},
@{V="15";T="The Probability of Gambling";C="Loophole";A="NPC + Faceless";S="v2.4: Probability Rights";E="Casino System Linked";O="Victory (Short)";F="Betting Log"},
@{V="16";T="The Art of Taxation";C="Resource Scarcity";A="Chain + Law";S="v2.5: Tax Redistribution";E="Tax Flow Tracking";O="Bitter Victory";F="Tax Forms"},
@{V="17";T="The Monopoly of Knowledge";C="Irreversible Harm";A="Adaptive + Narrative";S="v2.6: Education Stratification";E="Edu Data Monopoly";O="Failure";F="Admission Rules"},
@{V="18";T="The Price of Beauty";C="Compliance Trap";A="Narrative";S="v2.7: Aesthetic Norms";E="Consumerism Metrics";O="Stalemate";F="Ad Copy"},
@{V="19";T="The Commodity of Time";C="Loophole";A="NPC + Faceless";S="v2.8: Time Capital";E="Punch Clock Network";O="Victory";F="Timesheets"},
@{V="20";T="The Hypocrisy of Charity";C="Responsibility Chain";A="Narrative + Chain";S="v2.9: Charity PR";E="Aid Fund Flow";O="Reversal (Sarah Dies)";F="Crowdfunding Screens"},
@{V="21";T="The Paradox of Prediction";C="Resource Scarcity";A="Faceless (Model)";S="v3.0: Algorithmic Gov";E="Prediction Model Source";O="Failure";F="Pseudo-code"},
@{V="22";T="The Tampering of Memory";C="Irreversible Harm";A="Adaptive (History)";S="v3.1: Memory Rights";E="Archive Diff Versions";O="Stalemate";F="Version Diff Table"},
@{V="23";T="The Naked Privacy";C="Irreversible Harm";A="Chain + Adaptive";S="v3.2: Privacy Irreversible";E="Surveillance Map";O="Victory (Temp)";F="Map/GIS"},
@{V="24";T="The Calculus of Emotion";C="Loophole";A="Adaptive (Humanity)";S="v3.3: Emotion Incomputable";E="Matching Algo 104_C";O="Reversal";F="Chat Logs"},
@{V="25";T="The Harvest of Attention";C="Compliance Trap";A="Narrative + Faceless";S="v3.4: Attention Rights";E="Rec Algo Panorama";O="Failure (Sophie Dies)";F="Usage Stats"},
@{V="26";T="The Trial of Code";C="Responsibility Chain";A="Law + Adaptive";S="v3.5: Code is Law";E="AI Judge Code Leak";O="Bitter Victory";F="Judgment Record"},
@{V="27";T="The Theft of Identity";C="Irreversible Harm";A="Adaptive";S="v3.6: Virtual ID";E="ID DB Schema";O="Stalemate";F="DB Schema"},
@{V="28";T="The Island of Trust";C="Responsibility Chain";A="Chain (Atomized)";S="v3.7: Trust Collapse";E="Social Network Frag";O="Reversal";F="Report Chain"},
@{V="29";T="The Redundancy of Error";C="Loophole";A="Faceless (Bug)";S="v3.8: Bug is Fate";E="Original Code Snippet";O="Victory (Short)";F="Bug Tracker"},
@{V="30";T="The Delusion of Immortality";C="Irreversible Harm";A="Adaptive (Forever)";S="v3.9: No Immortality";E="System 30-Year Plan";O="Failure (Miller Dies)";F="Project Docs"},
@{V="31";T="The Edge of Chaos";C="Resource Scarcity";A="Adaptive (Pre-Collapse)";S="v4.0: Collapse Signals";E="System Contradictions";O="Stalemate";F="Error Logs"},
@{V="32";T="The Black Swan";C="Irreversible Harm";A="Chain + Adaptive";S="v4.1: Unpredictability";E="Surprise Victory Condition";O="Victory (Accident)";F="Accident Report"},
@{V="33";T="The Scapegoat";C="Responsibility Chain";A="Narrative (Blame)";S="v4.2: Naming Responsibility";E="Designer ID Surfaces";O="Reversal";F="Resignation Letter"},
@{V="34";T="The Ghost Revenge";C="Irreversible Harm";A="Adaptive (Memorial)";S="v4.3: History Inevitable";E="Dead Data Activation";O="Failure";F="Ghost Files"},
@{V="35";T="The Last Manual Labor";C="Loophole";A="Faceless (Auto Limit)";S="v4.4: Human Rights";E="When Humans Obsolete";O="Victory";F="Retirement Protocol"},
@{V="36";T="The Spiral of Silence";C="Compliance Trap";A="Narrative (Silence)";S="v4.5: Voice Rights";E="Suppression Tactics";O="Stalemate";F="Censorship Log"},
@{V="37";T="The Value of Uselessness";C="Irreversible Harm";A="Narrative + Adaptive";S="v4.6: Meaning Rights";E="Unpriceable Things";O="Reversal";F="Art Manifesto"},
@{V="38";T="The Algorithm of Love";C="Loophole";A="Adaptive (Love Calc)";S="v4.7: Love Incomputable";E="Love Logic Holes";O="Victory";F="Love Letters Collage"},
@{V="39";T="The Twilight of Mentors";C="Responsibility Chain";A="Chain (Education)";S="v4.8: Legacy Rights";E="Betrayal Proof";O="Reversal";F="Teacher-Student Letters"},
@{V="40";T="The Partisan Split";C="Resource Scarcity";A="Adaptive (Two Parties)";S="v4.9: Self-Awareness Rights";E="Partisan Funding Map";O="Failure (Absorption)";F="Internal Monologue"},
@{V="41";T="The Hearing";C="Irreversible Harm";A="System (Congress)";S="v4.10: Loop Fate";E="History Loop Proof";O="Stalemate";F="Timeline Comparison"},
@{V="42";T="The Remainder";C="Responsibility Chain";A="Adaptive (Ultimate)";S="v4.11: New Beginning";E="All Ends/Starts";O="Reversal (Cycle)";F="Final Signature"}
)

$template = @"
# 《未尽之算》卷{0}：{1} (v4.0)

**结构**：集{2}-{3} | 4小案 × 6集 = 24集 | **主题**：{1}
**核心**：{4} | **对手**：{5} | **形式**：{6}

---

## Part A: 卷级防疲劳签名 (Volume Signature)
| 维度 | 设定 |
|---|---|
| **案型** | {4} |
| **对手形态** | {5} |
| **标准升级** | {7} |
| **证据增量** | {8} |
| **结局类型** | {9} |
| **呈现形式** | {6} |

---

## Part B: 4小案结构 (24集骨架)

### 小案 1 (Ep {10}-{11})
*   **Docket (痒点)**: [待补充: 具体的{4}触发点]
*   **Evidence (取证)**: [待补充: {8}相关线索]
*   **Sophie (情感)**: [待补充: Sophie/Witness的情感锚点]
*   **Options (困境)**: [待补充: 三个两难选项]
*   **Court (执行)**: [待补充: 具体的反杀动作]
*   **Aftermath (后果)**: [待补充: 系统适应与{7}的铺垫]

### 小案 2 (Ep {12}-{13})
*   **Docket**: ...
*   **Evidence**: ...
*   **Options**: ...
*   **Court**: ...
*   **Aftermath**: ...

### 小案 3 (Ep {14}-{15})
*   **Docket**: ...
*   **Evidence**: ...
*   **Options**: ...
*   **Court**: ...
*   **Aftermath**: ...

### 小案 4 (Ep {16}-{3})
*   **Docket**: ...
*   **Evidence**: ...
*   **Options**: ...
*   **Court**: ...
*   **Aftermath**: ...

---

## Part C: 付费钩子 (The Adjudication Stack)
*   **Standard v1.x**: **{7}**
*   **Red Lines (红线)**: [待定义: 本卷的绝对禁区]
*   **Human Check (人性三测)**: Replaceable? / Dialogue? / Exit?
*   **Operational Questions**: Sustainable? / Survivable? / Exit Path?

---

## Part D: 过渡与埋种 (Transitions)
*   **上一卷**: ...
*   **下一卷钩子**: ...
*   **Mia的种子 (Mia's Seed)**: [待补充: Mia在本卷学到了什么?]

"@

foreach ($v in $vols) {
    $sEp = ([int]$v.V - 1) * 24 + 1
    $eEp = [int]$v.V * 24
    $c1e = $sEp + 5
    $c2s = $sEp + 6
    $c2e = $sEp + 11
    $c3s = $sEp + 12
    $c3e = $sEp + 17
    $c4s = $sEp + 18
    
    $txt = $template -f $v.V, $v.T, $sEp, $eEp, $v.C, $v.A, $v.F, $v.S, $v.E, $v.O, $sEp, $c1e, $c2s, $c2e, $c3s, $c3e, $c4s
    $path = "D:\_Progs\01Center\ASTO\小说故事\《未尽之算》-en\大纲集\卷$($v.V)-大纲.md"
    Set-Content -Path $path -Value $txt -Encoding UTF8
}
