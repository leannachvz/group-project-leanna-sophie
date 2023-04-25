circleManager = new CircleManager('circles');
circleManager.add("Friend 1!!!!");
circleManager.add("Person 2!!");
circleManager.add("Friend 3", 1000);
circleManager.add("Person 4!!!", 2000);
circleManager.add("Friend 5!!!!!", 5000);
circleManager.add("Person 6!", 10000);
circleManager.add("Friend 7!!!", 20000);

document.getElementById('button').onclick = () => {
    const input = document.getElementById('input');
    const text = input.value;
    input.value = "";
    if (text) {
        circleManager.add(text);
    }
}