import Item from "./Item"

const arr = ["恩",2,3]

const List = () => {
    return <div>
        <Item />
        <Item />
        <Item />
        {
            //arr.map(item => <Item />) 3個Item
            //arr.map(item => <div>{item}</div>) //arr 所有值
        }
    </div>
}

export default List