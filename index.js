
const f1 = () => {
  throw new Error('Hello')
}

const f2 = () => {
  f1()
}

const f3 = () => {
  f2()
}

f3()
