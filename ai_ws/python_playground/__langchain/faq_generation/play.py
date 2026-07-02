from typing import Any

from langchain_ollama import OllamaEmbeddings
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import normalize

embedding = OllamaEmbeddings(
    model="qwen3-embedding:8b",
    validate_model_on_init=True,
)

conversation_summaries: list[dict[str, Any]] = [
    # -----------------------------
    # Expected Cluster A: KYC pending / verification delay
    # -----------------------------
    {
        "conversation_id": "conv_001",
        "summary": "Customer asked why their KYC verification is still pending after uploading documents.",
        "status": "resolved",
        "created_at": "2026-06-30",
        "was_escalated": True,
        "category": "kyc",
        "expected_cluster": "kyc_pending",
    },
    {
        "conversation_id": "conv_002",
        "summary": "Customer wants to know why account verification has not been approved yet.",
        "status": "resolved",
        "created_at": "2026-06-29",
        "was_escalated": True,
        "category": "kyc",
        "expected_cluster": "kyc_pending",
    },
    {
        "conversation_id": "conv_003",
        "summary": "Customer submitted identity documents but their profile is still under review.",
        "status": "resolved",
        "created_at": "2026-06-28",
        "was_escalated": False,
        "category": "kyc",
        "expected_cluster": "kyc_pending",
    },
    {
        "conversation_id": "conv_004",
        "summary": "Customer asked how long document verification usually takes after submitting KYC files.",
        "status": "resolved",
        "created_at": "2026-06-27",
        "was_escalated": False,
        "category": "kyc",
        "expected_cluster": "kyc_pending",
    },
    {
        "conversation_id": "conv_005",
        "summary": "Customer says their account is not verified even though they already uploaded the required documents.",
        "status": "resolved",
        "created_at": "2026-06-26",
        "was_escalated": True,
        "category": "kyc",
        "expected_cluster": "kyc_pending",
    },
    # -----------------------------
    # Expected Cluster B: KYC document rejection / invalid documents
    # Similar category to A, but different intent.
    # This is useful to test whether clustering separates pending vs rejected.
    # -----------------------------
    {
        "conversation_id": "conv_006",
        "summary": "Customer asked why their proof of address document was rejected.",
        "status": "resolved",
        "created_at": "2026-06-25",
        "was_escalated": True,
        "category": "kyc",
        "expected_cluster": "kyc_rejected_documents",
    },
    {
        "conversation_id": "conv_007",
        "summary": "Customer wants to know why their uploaded ID document was not accepted.",
        "status": "resolved",
        "created_at": "2026-06-24",
        "was_escalated": False,
        "category": "kyc",
        "expected_cluster": "kyc_rejected_documents",
    },
    {
        "conversation_id": "conv_008",
        "summary": "Customer asked what to do after their verification document failed validation.",
        "status": "resolved",
        "created_at": "2026-06-23",
        "was_escalated": False,
        "category": "kyc",
        "expected_cluster": "kyc_rejected_documents",
    },
    {
        "conversation_id": "conv_009",
        "summary": "Customer says the system rejected their KYC upload and asks which document should be submitted instead.",
        "status": "resolved",
        "created_at": "2026-06-22",
        "was_escalated": True,
        "category": "kyc",
        "expected_cluster": "kyc_rejected_documents",
    },
    # -----------------------------
    # Expected Cluster C: Withdrawal pending / delayed withdrawal
    # -----------------------------
    {
        "conversation_id": "conv_010",
        "summary": "Customer asked why their withdrawal request is still pending.",
        "status": "resolved",
        "created_at": "2026-06-30",
        "was_escalated": True,
        "category": "withdrawal",
        "expected_cluster": "withdrawal_pending",
    },
    {
        "conversation_id": "conv_011",
        "summary": "Customer says their withdrawal has not arrived yet and asks when it will be processed.",
        "status": "resolved",
        "created_at": "2026-06-29",
        "was_escalated": True,
        "category": "withdrawal",
        "expected_cluster": "withdrawal_pending",
    },
    {
        "conversation_id": "conv_012",
        "summary": "Customer wants to know why cash-out is delayed after submitting a withdrawal request.",
        "status": "resolved",
        "created_at": "2026-06-28",
        "was_escalated": True,
        "category": "withdrawal",
        "expected_cluster": "withdrawal_pending",
    },
    {
        "conversation_id": "conv_013",
        "summary": "Customer asked why their withdrawal status remains under review.",
        "status": "resolved",
        "created_at": "2026-06-27",
        "was_escalated": False,
        "category": "withdrawal",
        "expected_cluster": "withdrawal_pending",
    },
    {
        "conversation_id": "conv_014",
        "summary": "Customer is concerned that their withdrawal request is taking longer than expected.",
        "status": "resolved",
        "created_at": "2026-06-26",
        "was_escalated": True,
        "category": "withdrawal",
        "expected_cluster": "withdrawal_pending",
    },
    # -----------------------------
    # Expected Cluster D: Withdrawal method / bank account issue
    # Same category as C, but different intent.
    # -----------------------------
    {
        "conversation_id": "conv_015",
        "summary": "Customer asked how to change the bank account used for withdrawals.",
        "status": "resolved",
        "created_at": "2026-06-25",
        "was_escalated": False,
        "category": "withdrawal",
        "expected_cluster": "withdrawal_bank_method",
    },
    {
        "conversation_id": "conv_016",
        "summary": "Customer wants to update their withdrawal payment method before submitting a request.",
        "status": "resolved",
        "created_at": "2026-06-24",
        "was_escalated": False,
        "category": "withdrawal",
        "expected_cluster": "withdrawal_bank_method",
    },
    {
        "conversation_id": "conv_017",
        "summary": "Customer asked whether they can withdraw funds to a different bank account.",
        "status": "resolved",
        "created_at": "2026-06-23",
        "was_escalated": False,
        "category": "withdrawal",
        "expected_cluster": "withdrawal_bank_method",
    },
    {
        "conversation_id": "conv_018",
        "summary": "Customer says their saved withdrawal account is incorrect and asks how to replace it.",
        "status": "resolved",
        "created_at": "2026-06-22",
        "was_escalated": True,
        "category": "withdrawal",
        "expected_cluster": "withdrawal_bank_method",
    },
    # -----------------------------
    # Expected Cluster E: Deposit failed / deposit not credited
    # -----------------------------
    {
        "conversation_id": "conv_019",
        "summary": "Customer asked why their deposit has not been credited to the trading account.",
        "status": "resolved",
        "created_at": "2026-06-30",
        "was_escalated": True,
        "category": "deposit",
        "expected_cluster": "deposit_not_credited",
    },
    {
        "conversation_id": "conv_020",
        "summary": "Customer says they made a payment but the deposit balance is still not showing.",
        "status": "resolved",
        "created_at": "2026-06-29",
        "was_escalated": True,
        "category": "deposit",
        "expected_cluster": "deposit_not_credited",
    },
    {
        "conversation_id": "conv_021",
        "summary": "Customer asked why funds sent through a deposit method have not appeared in their account.",
        "status": "resolved",
        "created_at": "2026-06-28",
        "was_escalated": False,
        "category": "deposit",
        "expected_cluster": "deposit_not_credited",
    },
    {
        "conversation_id": "conv_022",
        "summary": "Customer reported that their deposit transaction was successful but the account balance did not update.",
        "status": "resolved",
        "created_at": "2026-06-27",
        "was_escalated": True,
        "category": "deposit",
        "expected_cluster": "deposit_not_credited",
    },
    # -----------------------------
    # Expected Cluster F: Password reset / forgot password
    # -----------------------------
    {
        "conversation_id": "conv_023",
        "summary": "Customer forgot their password and asked how to reset it.",
        "status": "resolved",
        "created_at": "2026-06-21",
        "was_escalated": False,
        "category": "account",
        "expected_cluster": "password_reset",
    },
    {
        "conversation_id": "conv_024",
        "summary": "Customer cannot log in because they do not remember their password.",
        "status": "resolved",
        "created_at": "2026-06-20",
        "was_escalated": False,
        "category": "account",
        "expected_cluster": "password_reset",
    },
    {
        "conversation_id": "conv_025",
        "summary": "Customer asked where to find the forgot password option.",
        "status": "resolved",
        "created_at": "2026-06-19",
        "was_escalated": False,
        "category": "account",
        "expected_cluster": "password_reset",
    },
    {
        "conversation_id": "conv_026",
        "summary": "Customer wants instructions for resetting their login password.",
        "status": "resolved",
        "created_at": "2026-06-18",
        "was_escalated": False,
        "category": "account",
        "expected_cluster": "password_reset",
    },
    # -----------------------------
    # Expected Cluster G: Login problem / account access issue
    # Close to password reset, but not exactly the same.
    # Good test for over-grouping.
    # -----------------------------
    {
        "conversation_id": "conv_027",
        "summary": "Customer says they cannot log in even though they entered the correct password.",
        "status": "resolved",
        "created_at": "2026-06-26",
        "was_escalated": True,
        "category": "account",
        "expected_cluster": "login_issue",
    },
    {
        "conversation_id": "conv_028",
        "summary": "Customer asked why login fails after entering valid account credentials.",
        "status": "resolved",
        "created_at": "2026-06-25",
        "was_escalated": True,
        "category": "account",
        "expected_cluster": "login_issue",
    },
    {
        "conversation_id": "conv_029",
        "summary": "Customer reported an error message when trying to access the client portal.",
        "status": "resolved",
        "created_at": "2026-06-24",
        "was_escalated": True,
        "category": "account",
        "expected_cluster": "login_issue",
    },
    {
        "conversation_id": "conv_030",
        "summary": "Customer says the platform does not allow them to sign in to their account.",
        "status": "resolved",
        "created_at": "2026-06-23",
        "was_escalated": False,
        "category": "account",
        "expected_cluster": "login_issue",
    },
    # -----------------------------
    # Expected Cluster H: Trading platform download / installation
    # -----------------------------
    {
        "conversation_id": "conv_031",
        "summary": "Customer asked where to download the trading platform.",
        "status": "resolved",
        "created_at": "2026-06-22",
        "was_escalated": False,
        "category": "platform",
        "expected_cluster": "platform_download",
    },
    {
        "conversation_id": "conv_032",
        "summary": "Customer wants the installation link for the trading terminal.",
        "status": "resolved",
        "created_at": "2026-06-21",
        "was_escalated": False,
        "category": "platform",
        "expected_cluster": "platform_download",
    },
    {
        "conversation_id": "conv_033",
        "summary": "Customer asked how to install the trading application on their computer.",
        "status": "resolved",
        "created_at": "2026-06-20",
        "was_escalated": False,
        "category": "platform",
        "expected_cluster": "platform_download",
    },
    {
        "conversation_id": "conv_034",
        "summary": "Customer requested help downloading the mobile trading app.",
        "status": "resolved",
        "created_at": "2026-06-19",
        "was_escalated": False,
        "category": "platform",
        "expected_cluster": "platform_download",
    },
    # -----------------------------
    # Expected Cluster I: Leverage change
    # -----------------------------
    {
        "conversation_id": "conv_035",
        "summary": "Customer asked how to change leverage on their trading account.",
        "status": "resolved",
        "created_at": "2026-06-18",
        "was_escalated": False,
        "category": "trading_account",
        "expected_cluster": "leverage_change",
    },
    {
        "conversation_id": "conv_036",
        "summary": "Customer wants to increase the leverage setting for an existing account.",
        "status": "resolved",
        "created_at": "2026-06-17",
        "was_escalated": True,
        "category": "trading_account",
        "expected_cluster": "leverage_change",
    },
    {
        "conversation_id": "conv_037",
        "summary": "Customer asked whether account leverage can be adjusted after registration.",
        "status": "resolved",
        "created_at": "2026-06-16",
        "was_escalated": False,
        "category": "trading_account",
        "expected_cluster": "leverage_change",
    },
    {
        "conversation_id": "conv_038",
        "summary": "Customer says they selected the wrong leverage and wants to modify it.",
        "status": "resolved",
        "created_at": "2026-06-15",
        "was_escalated": False,
        "category": "trading_account",
        "expected_cluster": "leverage_change",
    },
    # -----------------------------
    # Expected Cluster J: Promotion / bonus eligibility
    # -----------------------------
    {
        "conversation_id": "conv_039",
        "summary": "Customer asked whether they are eligible for the current deposit bonus.",
        "status": "resolved",
        "created_at": "2026-06-14",
        "was_escalated": False,
        "category": "promotion",
        "expected_cluster": "bonus_eligibility",
    },
    {
        "conversation_id": "conv_040",
        "summary": "Customer wants to know why they did not receive the promotion bonus.",
        "status": "resolved",
        "created_at": "2026-06-13",
        "was_escalated": True,
        "category": "promotion",
        "expected_cluster": "bonus_eligibility",
    },
    {
        "conversation_id": "conv_041",
        "summary": "Customer asked what conditions must be met to claim the trading bonus.",
        "status": "resolved",
        "created_at": "2026-06-12",
        "was_escalated": False,
        "category": "promotion",
        "expected_cluster": "bonus_eligibility",
    },
    {
        "conversation_id": "conv_042",
        "summary": "Customer asked if their account type qualifies for a promotional offer.",
        "status": "resolved",
        "created_at": "2026-06-11",
        "was_escalated": False,
        "category": "promotion",
        "expected_cluster": "bonus_eligibility",
    },
    # -----------------------------
    # Expected noise / should not form strong FAQ clusters
    # -----------------------------
    {
        "conversation_id": "conv_043",
        "summary": "Customer greeted the agent and did not ask a specific question.",
        "status": "resolved",
        "created_at": "2026-06-10",
        "was_escalated": False,
        "category": "general",
        "expected_cluster": "noise",
    },
    {
        "conversation_id": "conv_044",
        "summary": "Customer thanked the support team for helping with a previous issue.",
        "status": "resolved",
        "created_at": "2026-06-09",
        "was_escalated": False,
        "category": "general",
        "expected_cluster": "noise",
    },
    {
        "conversation_id": "conv_045",
        "summary": "Customer asked whether the company has an office in a specific city.",
        "status": "resolved",
        "created_at": "2026-06-08",
        "was_escalated": False,
        "category": "general",
        "expected_cluster": "noise",
    },
    {
        "conversation_id": "conv_046",
        "summary": "Customer asked for a human agent without explaining the issue.",
        "status": "resolved",
        "created_at": "2026-06-07",
        "was_escalated": True,
        "category": "general",
        "expected_cluster": "noise",
    },
    {
        "conversation_id": "conv_047",
        "summary": "Customer asked about career opportunities and job openings.",
        "status": "resolved",
        "created_at": "2026-06-06",
        "was_escalated": True,
        "category": "general",
        "expected_cluster": "noise",
    },
]


def embed_summaries(conversations: list[dict[str, str]]) -> np.ndarray:
    texts = [item["summary"] for item in conversations]

    vectors = embedding.embed_documents(texts)

    return np.array(vectors)


vectors = embed_summaries(conversation_summaries)


def cluster_summaries(
    vectors: np.ndarray,
    eps: float = 0.25,
    min_samples: int = 2,
) -> np.ndarray:
    """
    Returns cluster labels.

    Example:
    [0, 0, 0, 1, 1, 2, 2]

    - Same number = same cluster
    - -1 = noise / no clear cluster
    """

    normalized_vectors = normalize(vectors)

    clustering = DBSCAN(
        eps=eps,
        min_samples=min_samples,
        metric="cosine",
    )

    labels = clustering.fit_predict(normalized_vectors)

    return labels


labels = cluster_summaries(vectors)

for item, label in zip(conversation_summaries, labels):
    print(label, item["summary"])
