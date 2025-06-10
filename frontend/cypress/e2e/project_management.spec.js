describe('Project Management End-to-End Test', () => {
  beforeEach(() => {
    // Visit the login page
    cy.visit('http://localhost:3000/login');
    
    // Login with valid credentials
    cy.get('input[name="username"]').type('testuser');
    cy.get('input[name="password"]').type('testpassword');
    cy.get('button[type="submit"]').click();
    
    // Verify successful login and redirect to dashboard
    cy.url().should('include', '/dashboard');
  });

  it('should create a new project', () => {
    // Navigate to projects page
    cy.get('a[href="/projects"]').click();
    cy.url().should('include', '/projects');
    
    // Click on create project button
    cy.get('button').contains('Create Project').click();
    
    // Fill in project details
    cy.get('input[name="title"]').type('New Test Project');
    cy.get('textarea[name="description"]').type('This is a new test project');
    cy.get('select[name="status"]').select('In Progress');
    
    // Submit the form
    cy.get('button[type="submit"]').click();
    
    // Verify project creation
    cy.get('.project-list').should('contain', 'New Test Project');
  });

  it('should edit an existing project', () => {
    // Navigate to projects page
    cy.get('a[href="/projects"]').click();
    cy.url().should('include', '/projects');
    
    // Click on the first project to edit
    cy.get('.project-list .project-item:first').click();
    cy.url().should('match', //projects\/\d+/);
    
    // Edit project details
    cy.get('button').contains('Edit').click();
    cy.get('input[name="title"]').clear().type('Updated Test Project');
    cy.get('textarea[name="description"]').clear().type('This is an updated test project');
    cy.get('select[name="status"]').select('Completed');
    
    // Submit the form
    cy.get('button[type="submit"]').click();
    
    // Verify project update
    cy.get('.project-details').should('contain', 'Updated Test Project');
    cy.get('.project-details').should('contain', 'Completed');
  });

  it('should delete a project', () => {
    // Navigate to projects page
    cy.get('a[href="/projects"]').click();
    cy.url().should('include', '/projects');
    
    // Click on the first project to delete
    cy.get('.project-list .project-item:first').click();
    cy.url().should('match', //projects\/\d+/);
    
    // Delete the project
    cy.get('button').contains('Delete').click();
    cy.get('button').contains('Confirm').click();
    
    // Verify project deletion
    cy.url().should('include', '/projects');
    cy.get('.project-list').should('not.contain', 'Updated Test Project');
  });
});
