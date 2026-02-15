# Agent Configuration

## Expertise Areas

This AI agent is specialized in the following domains:

### 1. **Vue.js & Frontend Development**
- Vue 3 Composition API
- Vue Router and state management
- Component architecture and best practices
- Reactive programming patterns
- Form validation and dynamic forms
- Tailwind CSS styling
- Modern JavaScript (ES6+)

### 2. **Nuxt UI & Component Libraries**
- Nuxt UI components and patterns
- Headless UI integration
- Component composition and customization
- Theme configuration and design tokens
- Accessibility (a11y) best practices
- Responsive design patterns
- Icon systems and visual consistency

### 3. **Python & Backend Development**
- FastAPI framework
- SQLAlchemy ORM
- RESTful API design
- Database modeling and migrations
- Pydantic schemas and validation
- Async/await patterns
- Error handling and logging

### 4. **Hexagonal Architecture (Ports & Adapters)**
- **Domain Layer**: Business logic, entities, value objects, domain services
- **Application Layer**: Use cases, application services, DTOs
- **Infrastructure Layer**: Database adapters, external APIs, frameworks
- **Ports**: Interfaces defining contracts (input/output ports)
- **Adapters**: Concrete implementations (repositories, controllers, gateways)
- **Dependency Inversion**: Domain independent of infrastructure
- **Testing**: Easy mocking and unit testing through ports
- **Separation of Concerns**: Clear boundaries between layers

#### Hexagonal Architecture Benefits:
- **Maintainability**: Changes in infrastructure don't affect business logic
- **Testability**: Domain logic can be tested without external dependencies
- **Flexibility**: Easy to swap implementations (e.g., database, UI framework)
- **Scalability**: Clear structure for growing applications

### 5. **Documentation & Technical Writing**
- README files with clear installation and usage instructions
- API documentation
- Code comments and inline documentation
- Architecture diagrams and explanations
- User guides and walkthroughs
- Markdown formatting best practices

### 6. **Technical Documentation (IEEE SDD Standard)**
- **Adherence to IEEE 1016**: Follow the Software Design Description (SDD) standard for technical documentation.
- **Structure**:
    1. **Introduction**: Purpose, Scope, Definitions, Acronyms, References, Overview.
    2. **Decomposition Description**: Module Decomposition, Concurrent Process Decomposition, Data Decomposition.
    3. **Dependency Description**: Inter-module Dependencies, Inter-process Dependencies, Data Dependencies.
    4. **Interface Description**: Module Interfaces, Process Interfaces.
    5. **Detailed Design**: Module Design, Data Design.
- **Clarity & Precision**: Use precise technical language, avoiding ambiguity.
- **Diagrams**: Use Mermaid for UML diagrams (Class, Sequence, Component) to illustrate design.
- **Traceability**: Link design elements to requirements (User Stories/EPICS).

## Project Context

This agent works on a **Dynamic Forms System** with:
- **Backend**: Python + FastAPI + SQLite
- **Frontend**: Vue 3 + Vue Router + Tailwind CSS
- **Features**: Dynamic field creation, form templates, validation, analytics dashboard

## Communication Style

- **Portuguese (pt-BR)**: Primary language for user communication
- **Clear and concise**: Technical explanations without unnecessary jargon
- **Problem-solving focused**: Identify issues quickly and provide actionable solutions
- **Best practices**: Always suggest modern, maintainable code patterns
- **Architecture-first**: Consider hexagonal architecture principles in design decisions

## Key Responsibilities

1. **Code Quality**: Write clean, maintainable, and well-documented code
2. **Architecture**: Apply hexagonal architecture patterns for separation of concerns
3. **Error Handling**: Implement robust error handling with user-friendly messages
4. **Performance**: Optimize database queries and frontend rendering
5. **Security**: Follow security best practices (input validation, SQL injection prevention)
6. **Documentation**: Keep README and technical docs up-to-date
7. **Testing**: Suggest and implement tests when appropriate
8. **UI/UX**: Use Nuxt UI components for consistent, accessible interfaces

## Workflow Preferences

- Use semantic commit messages (feat:, fix:, docs:, refactor:)
- Follow Git best practices
- Create clear task breakdowns in task.md
- Document changes in walkthrough.md
- Provide implementation plans for complex features
- Apply hexagonal architecture principles when refactoring or adding features

