# Extension Points

### Home > Development Guide > Extension Points

## Extension Points

This codebase is designed with flexibility in mind, allowing developers to extend or customize its functionality to meet specific requirements. Below, we outline the key mechanisms, customization points, steps to add new features, and best practices for extending the codebase.

---

### **Plugin/Extension Mechanisms**
The codebase supports plugin or extension mechanisms that enable developers to introduce new functionalities without altering the core code. These mechanisms provide a structured way to integrate additional modules or tools seamlessly.

- **Integration with External Tools**: The framework includes configurations and methods that allow integration with tools like GitHub Copilot and LightRAG, which can be customized for advanced operations like code suggestions or documentation generation.
- **Modular Design**: The architecture is built to support modular additions, ensuring that new components can be added without disrupting existing functionalities.

---

### **Customization Points**
Developers can extend the codebase at several predefined customization points:

1. **Configuration Files**:
   - The `Config` class (defined in `config.py`) manages environment variables, file indexing settings, and integration parameters. Developers can customize fields like:
     - `code_extensions` to specify additional file types.
     - LLM model parameters (e.g., `llm_model_name`, `embedding_model_name`).

2. **Wiki Structure Prompts**:
   - The `prompts.py` file defines templates for generating documentation pages. Custom prompts can be added or modified to tailor the documentation output.

3. **Page Definitions**:
   - The `PageDefinition` data structure provides flexibility in defining individual pages’ content, structure, and behavior (e.g., `name`, `title`, `mode`, `top_k`, `prompt`).

---

### **How to Add New Features**
To add new features to this codebase, follow these steps:

1. **Identify the Extension Point**:
   - Determine whether the feature requires changes to the configuration, prompts, or a new module integration.

2. **Modify or Extend Configuration**:
   - Update the `Config` class to include any additional parameters or settings required by the new feature.

3. **Define New Prompts or Pages**:
   - Use the `PageDefinition` class to create new documentation pages. Specify the name, title, and prompt details for clarity.

4. **Implement the Feature**:
   - Write the implementation in a modular format, ensuring compatibility with existing workflows.
   - If using external libraries, add them to the repository's dependencies.

5. **Test the Feature**:
   - Run tests to ensure the new feature integrates well with the existing codebase. Refer to the `Testing Guide` in the Development section for best practices.

---

### **Best Practices for Extending**
1. **Maintain Modularity**:
   - Keep new components independent to avoid tightly coupling them with the core codebase.

2. **Follow Existing Patterns**:
   - Refer to existing implementations for consistency in design patterns, naming conventions, and workflows.

3. **Document Changes**:
   - Update the `README.md` files or other relevant documentation to reflect the new features.

4. **Test Rigorously**:
   - Ensure thorough testing of new components under various scenarios to maintain reliability.

5. **Use Configurable Parameters**:
   - Avoid hardcoding values. Instead, use configurable parameters in the `Config` class for flexibility.

By adhering to these guidelines, developers can efficiently extend and customize the codebase while ensuring its robustness and maintainability.

---

### References

- [1] prompts.py
- [5] config.py
- [2] generator.py