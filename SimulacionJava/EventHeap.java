
public class EventHeap {
	Event[] heapArray;
	int entries;
	
	public EventHeap(int size) {
		heapArray=new Event[size];
		entries=0;
	}
	
	private int parent(int n) {
		return (n-1)/2;
	}
	
	private int leftChild(int n) {
		return 2*n+1;
	}
	
	private int rightChild(int n) {
		return 2*n+2;
	}
	
	public boolean isEmpty() {
		return (entries==0);
	}
	
	public Event peek() {
		return heapArray[0];
	}
	
	private void swap(int i, int j) {
		Event temp=heapArray[i];
		heapArray[i]=heapArray[j];
		heapArray[j]=temp;
	}
	
	public void insert(Event item) {
		heapArray[entries++]=item; // add item to end of heap
		trickleUp(entries-1); // restore order
	}

	private void trickleUp(int n) {
		if (n==0) { // reached top of heap - done
			return;
		}
		if (heapArray[n].getTime()<heapArray[parent(n)].getTime()) { // check if parent is larger
			swap(n,parent(n)); // if so, swap 
			trickleUp(parent(n)); // recurse
		}
	}
	
	public Event remove() {
		Event item=heapArray[0]; // copy item from top of heap
		heapArray[0]=heapArray[--entries]; // move last item to top
		trickleDown(0); // restore order
		return item; // return former top item
	}
	
	private void trickleDown(int n) {
		if (leftChild(n)>=entries) { // n is a leaf node
			return;
		}
		if (rightChild(n)>=entries) { // n has a left child
			if (heapArray[n].getTime()>heapArray[leftChild(n)].getTime()) { // swap with left child
				swap(n,leftChild(n));
				trickleDown(leftChild(n)); // recurse
			}
			return;
		}
		// n has two children
		if (heapArray[n].getTime()>heapArray[leftChild(n)].getTime() || heapArray[n].getTime()>heapArray[rightChild(n)].getTime()) { // need to continue trickling down
			if (heapArray[leftChild(n)].getTime()<heapArray[rightChild(n)].getTime()) { // swap with left child
				swap(n,leftChild(n));
				trickleDown(leftChild(n)); // recurse
			} else { // swap with right child
				swap(n,rightChild(n));
				trickleDown(rightChild(n)); // recurse
			}
		}
	}
	
	
	public String toString() {
		String s="heap:";
		for (int i=0; i<entries; i++) {
			s+=" "+heapArray[i];
		}
		return s;
	}
	
}
