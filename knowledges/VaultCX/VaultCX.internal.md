# MH-VaultCX Internal Usage Guide

## Internal Usage Overview

This knowledge base is for internal users who need help using MH-VaultCX features inside the platform.

It covers common internal tasks such as:

- navigating the admin portal
- creating and managing domains
- editing prompts
- ingesting knowledge sources
- configuring tools
- managing model integrations
- accessing the AI chat panel
- using the human agent panel
- configuring the embeddable chat widget

---

## Platform Navigation

### Main Navigation Areas

The MH-VaultCX internal portal includes the following main navigation areas:

- Dashboard
- Organization Management
- Domains
- Prompt Studio
- Knowledge Hub
- Tool Integrations
- Model Integrations
- AI Chat Panel
- Human Agent Panel
- Widget Settings
- Analytics
- Settings

### Dashboard

The Dashboard provides a summary of an organization activity, recent conversations, domain status, and system notifications.

### Organization Management

Organization Management is used to view organization workspaces, registration details, plan information, and account status.

### Domains

The Domains menu is used to create, edit, activate, and manage organization domains.

### Prompt Studio

Prompt Studio is used to create and maintain system prompts and behavior instructions for domains.

### Knowledge Hub

Knowledge Hub is used to upload, connect, index, and manage knowledge sources.

### Tool Integrations

Tool Integrations is used to register, configure, and maintain tools available to domains.

### Model Integrations

Model Integrations is used to configure foundation model connections and assign models to domains.

### Human Agent Panel

The Human Agent Panel is used by support agents to receive escalated conversations and communicate directly with customers.

### Widget Settings

Widget Settings is used to configure website chat widget behavior, appearance, and deployment settings.

---

## Domain Management

### How to Register a Domain

To register a new domain:

1. Sign in to the MH-VaultCX internal portal.
2. Open the **Domains** menu from the main navigation.
3. Click **Create Domain**.
4. Enter the domain name.
5. Enter the domain description.
6. Save the domain.

### Domain Creation Result

After a domain is created, it becomes available for prompt configuration, knowledge ingestion, tool assignment, and model assignment.

### How to Edit a Domain

To edit an existing domain:

1. Open the **Domains** menu.
2. Select the target domain from the domain list.
3. Click **Edit Domain**.
4. Update the domain details as needed.
5. Save changes.

### How to Activate or Deactivate a Domain

To change domain status:

1. Open the **Domains** menu.
2. Select the target domain.
3. Open the domain action menu.
4. Choose **Activate** or **Deactivate**.

### Domain Configuration Scope

Each domain can be configured with:

- prompt settings
- knowledge sources
- tools
- foundation model
- handoff behavior
- response rules

---

## Prompt Management

### How to Configure a Prompt

To configure a domain prompt:

1. Open **Prompt Studio** from the main navigation.
2. Select the target domain.
3. Open the active system prompt.
4. Edit the prompt content.
5. Save the prompt.
6. Publish the prompt if publishing is required.

### Prompt Types

Prompt Studio may contain:

- system prompts
- behavior prompts
- tool usage instructions
- handoff instructions
- response style guidance

### How to Update Prompt Instructions

To update prompt instructions:

1. Go to **Prompt Studio**.
2. Open the target prompt.
3. Modify the required instruction block.
4. Save changes.
5. Validate prompt behavior in the AI Chat Panel.

### Prompt Testing Recommendation

After prompt changes, internal users should test the domain in the AI Chat Panel before releasing the update to production.

---

## Knowledge Ingestion

### How to Ingest a Knowledge Source

To ingest a knowledge source:

1. Open **Knowledge Hub**.
3. Select the target domain.
4. Click **Add Source**.
5. Choose the source type.
6. Upload the file or connect the external source.
7. Confirm ingestion.
8. Wait for indexing to complete.

### Supported Knowledge Source Types

Knowledge Hub may support:

- markdown documents
- PDF files
- FAQ content
- help center articles
- policy documents
- internal SOPs
- web content
- connected external sources

### How to View Ingestion Status

To check ingestion progress:

1. Open **Knowledge Hub**.
2. Open the domain source list.
3. Review the ingestion status column.

Typical source statuses include:

- Pending
- Indexing
- Active
- Failed

### How to Reindex a Source

To reindex a source:

1. Open **Knowledge Hub**.
2. Select the source.
3. Open source actions.
4. Click **Reindex**.

### How to Remove a Source

To remove a source:

1. Open **Knowledge Hub**.
2. Select the source.
3. Open source actions.
4. Click **Remove Source**.
5. Confirm removal.

---

## Tool Integration

### How to Register a Tool

To register a tool:

1. Open **Tool Integrations**.
2. Click **Add Tool**.
3. Enter the tool name.
4. Enter the tool description.
5. Configure the execution details.
6. Save the tool configuration.

### Tool Registration Purpose

Registered tools can be assigned to one or more domains to extend domain capabilities.

### How to Assign a Tool to a Domain

To assign a tool to a domain:

1. Open **Domains**.
2. Select the target domain.
3. Open the **Tools** tab.
4. Click **Assign Tool**.
5. Select the desired tool.
6. Save changes.

### How to Edit a Tool

To edit a tool:

1. Open **Tool Integrations**.
2. Select the target tool.
3. Click **Edit Tool**.
4. Update configuration.
5. Save changes.

---

## Model Integration

### How to Connect a Foundation Model

To connect a foundation model:

1. Open **Model Integrations**.
2. Click **Add Model Integration**.
3. Select the model provider.
4. Enter the required connection settings.
5. Test the connection.
6. Save the integration.

### How to Assign a Model to a Domain

To assign a model to a domain:

1. Open **Domains**.
2. Select the target domain.
3. Open the **Model Settings** tab.
4. Select the preferred model integration.
5. Save the configuration.

### Model Assignment Recommendation

Each domain should have a validated model assignment before production use.

---

## AI Chat Panel

### How to Access the AI Chat Panel

To access the AI Chat Panel:

1. Open **AI Chat Panel** from the main navigation.
3. Select the target domain.
4. Start a test conversation.

### AI Chat Panel Purpose

The AI Chat Panel is used to:

- preview agent behavior
- validate prompt changes
- verify knowledge retrieval
- test tool usage
- simulate customer interactions

### Recommended Use of AI Chat Panel

Internal users should use the AI Chat Panel after:

- prompt updates
- knowledge ingestion changes
- tool registration changes
- model assignment changes

---

## Human Agent Panel

### How to Access the Human Agent Panel

To access the Human Agent Panel:

1. Open **Human Agent Panel** from the main navigation.

### Human Agent Panel Purpose

The Human Agent Panel is used to:

- receive escalated conversations
- review customer context
- continue conversations after handoff
- provide direct human support

### How to Handle an Escalated Conversation

To handle an escalated conversation:

1. Open **Human Agent Panel**.
2. Select the assigned conversation.
3. Review the conversation history.
4. Review the handoff summary.
5. Continue the conversation with the customer.

---

## Widget Configuration

### How to Configure the Embeddable Chat Widget

To configure the embeddable chat widget:

1. Open **Widget Settings**.
3. Open the target widget profile.
4. Configure appearance settings.
5. Configure chat behavior settings.
6. Save changes.

### How to Deploy the Widget

To deploy the widget:

1. Open **Widget Settings**.
2. Open the deployment section.
3. Copy the generated embed code.
4. Place the code in the target website page.
5. Publish the website update.

### Widget Deployment Verification

After deployment, verify that:

- the widget loads correctly
- the correct domain is connected
- AI responses are working
- handoff flow works if enabled


