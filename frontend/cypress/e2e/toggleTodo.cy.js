
// R8UC2
describe('toggle todo item', () => {

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
        })
    })
  })

  before(function () {


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

  it('todo item is struck through after icon is clicked', () => {

    cy.get('li.todo-item')
    .get('span.checker').eq(0)
    .click()
    
    cy.wait(200)

    cy.get('li.todo-item')
    .get('span.checker')
    .should('have.class', 'checked')

  })

  it('todo item is not struck through after icon is clicked again', () => {

    cy.get('li.todo-item')
    .get('span.checker').eq(0)
    .click()
    
    cy.wait(200)
    
    cy.get('li.todo-item')
    .get('span.checker').eq(0)
    .click()
    
    cy.wait(200)

    cy.get('li.todo-item')
    .get('span.checker')
    .should('not.have.class', 'checked')

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