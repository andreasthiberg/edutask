
// R8UC1
describe('add todo item', () => {

  let uid

  before(function () {
    cy.fixture('user.json')
      .then((user) => {
        cy.request({
          method: 'POST',
          url: "localhost:5000/users/create",
          form: true,
          body: user
        }).then((response) => {
          uid = response.body._id.$oid
          name = user.firstName + ' ' + user.lastName
          cy.fixture('task.json')
          .then((task) => {
            task.userid = uid;
            cy.request({
                method: 'POST',
                url: "localhost:5000/tasks/create",
                form: true,
                body: task,
      
           })
          })
        })
    })
  })


  beforeEach(function () {
    cy.visit('localhost:3000')
    cy.get('.inputwrapper #email')
      .type('jd@email.com')
    cy.get('form')
      .submit()
    cy.get('.container-element').eq(0)
      .find('a')
      .click()
  })

  it('add todo button is disabled when input field is empty', () => {

    cy.get('.inline-form')
    .find('input[type=submit]')
    .should('be.disabled')

  })

  it('successfully adds todo item with description', () => {
    cy.get('.inline-form')
    .find('input[type=text]')
    .type('make notes')

    cy.get('.inline-form')
    .find('input[type=submit]')
    .click()

    cy.get('.todo-item').eq(1)
    .should('contain.text', 'make notes')
  })

  after(function () {

    cy.request({
      method: 'DELETE',
      url: `localhost:5000/users/${uid}`
    }).then((response) => {
      cy.log(response.body)
    })
  })



})