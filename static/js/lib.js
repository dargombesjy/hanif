class PubSub {
    constructor() {
        this.events = {};
    }

    subscribe(ev, callback) {
        let self = this;
        if (!self.events.hasOwnProperty(ev)) {
            self.events[ev] = [];
        }

        return self.events[ev].push(callback);
    }

    publish(ev, data = {}) {
        let self = this;
        if (!self.events.hasOwnProperty(ev)) {
            return [];
        }

        return self.events[ev].map(callback => callback(data));
    }
}

class Store {
    constructor(params) {
        let self = this;
        self.actions = {};
        self.mutations = {}
        self.state = {};
        self.status = 'resting';
        self.events = new PubSub();
        if (params.hasOwnProperty('actions')) {
            self.actions = params.actions;
        }
        if (params.hasOwnProperty('mutations')) {
            self.mutations = params.mutations;
        }

        self.state = new Proxy(params.state || {}, {
            set: function (state, key, value) {
                state[key] = value;
                console.log(`statsChange: ${key}: ${value}`);
                self.events.publish('stateChange', self.state);
                if (self.status !== 'mutation') {
                    console.warn(`you should use a mutation to set ${key}`);
                }
                self.status = 'resting';
                return true;
            }
        });
    }

    dispatch(actionKey, payload) {
        let self = this;
        if (typeof self.actions[actionKey] !== 'function') {
            console.error(`Action "${actionKey} doesn't exist.`);
            return false;
        }
        console.groupCollapsed(`ACTION: ${actionKey}`);
        self.status = 'action';
        self.actions[actionKey](self, payload);
        console.groupEnd();
        return true;
    }

    commit(mutationKey, payload) {
        let self = this;
        if (typeof self.mutations[mutationKey] !== 'function') {
            console.log(`Mutation "${mutationKey}" doesn't exist`);
            return false;
        }
        self.status = 'mutation';
        let newState = self.mutations[mutationKey](self.state, payload);
        self.state = Object.assign(self.state, newState);
        return true;
    }

}

class Component {
    constructor(props = {}) {
        let self = this;
        this.render = this.render || function () { };
        if (props.store instanceof Store) {
            props.store.events.subscribe('stateChange', () => self.render());
        }
        if (props.hasOwnProperty('element')) {
            this.element = props.element;
        }
    }
}


let getSiblings = function (e) {
    let siblings = [];

    if (!e.parentNode) {
        return siblings;
    }
    // first child of the parent node
    let sibling = el.parentNode.firstChild;
    // collect siblings
    while (sibling) {
        if (sibling.nodeType === 1 && sibling !== e) {
            siblings.push(sibling);
        }
        sibling = sibling.nextSibling;
    }
    return siblings;
}