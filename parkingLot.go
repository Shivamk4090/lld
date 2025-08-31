package main

import (
	"errors"
	"fmt"
	"sync"
	"time"
)

type VehicleType int

const (
	CAR VehicleType = iota
	MOTORCYCLE
	TRUCK
)

type Vechile struct {
	license_plate string
	vType         VehicleType
}

func NewCar(license_plate string) *Vechile {
	return &Vechile{license_plate, CAR}
}

func NewMotorcycle(license_plate string) *Vechile {
	return &Vechile{license_plate, MOTORCYCLE}
}

func NewTruck(license_plate string) *Vechile {
	return &Vechile{license_plate, TRUCK}
}

type ParkingSpot struct {
	spot_id  int
	spotType VehicleType
	occupied bool
	mu       sync.Mutex
}

func (p *ParkingSpot) IsAvailable() bool {
	return !p.occupied
}

func (p *ParkingSpot) Park(vechile *Vechile) (int, error) {
	p.mu.Lock()
	defer p.mu.Unlock()

	if p.IsAvailable() && p.spotType == vechile.vType {
		p.occupied = true
		return p.spot_id, nil
	}
	return -1, errors.New("spot already occupied")
}

func (p *ParkingSpot) Leave() {
	p.mu.Lock()
	defer p.mu.Unlock()

	p.occupied = false
}

type Level struct {
	floor int
	spots []*ParkingSpot
}

func (l *Level) Park(vechile *Vechile) (int, error) {
	for _, spot := range l.spots {
		id, err := spot.Park(vechile)
		if err == nil {
			return id, nil
		}
	}
	return -1, errors.New("no spot available for this vehicle type")
}
func (l *Level) Exit(spotID int) error {
	for _, spot := range l.spots {
		if spot.spot_id == spotID {
			spot.Leave()
			return nil
		}
	}
	return errors.New("invalid spot ID")
}
func (l *Level) ListAvailibilty() int {
	ans := 0
	for _, spot := range l.spots {
		if spot.IsAvailable() {
			ans++
		}
	}
	return ans
}

type ParkingLot struct {
	levels []*Level
}

func (p *ParkingLot) Park(vechile *Vechile) (int, error) {
	for _, level := range p.levels {
		id, err := level.Park(vechile)
		if err == nil {
			return id, nil
		}
	}
	return -1, errors.New("no spot available for this vehicle type")
}
func (p *ParkingLot) Exit(spotID int) error {
	for _, level := range p.levels {
		err := level.Exit(spotID)
		if err == nil {
			return nil
		}
	}
	return errors.New("spot not found in any level")
}
func (p *ParkingLot) DisplayAvailibilty() {
	for _, level := range p.levels {
		fmt.Printf("Level %d => %d\n", level.floor, level.ListAvailibilty())
	}
}

func main() {
	ps1 := &ParkingSpot{spot_id: 1, spotType: CAR, occupied: false}
	ps2 := &ParkingSpot{spot_id: 2, spotType: MOTORCYCLE, occupied: false}
	ps3 := &ParkingSpot{spot_id: 3, spotType: TRUCK, occupied: false}

	level1 := &Level{floor: 1, spots: []*ParkingSpot{ps1, ps3}}
	level2 := &Level{floor: 2, spots: []*ParkingSpot{ps2}}

	parkingLot := &ParkingLot{levels: []*Level{level1, level2}}

	//

	v1 := NewCar("1234")
	v2 := NewCar("12345")

	parkingLot.DisplayAvailibilty()

	go func() {
		id, err := parkingLot.Park(v1)
		fmt.Println("Gate A => Car 1234 parked:", id, "err:", err)
	}()

	go func() {
		id, err := parkingLot.Park(v2)
		fmt.Println("Gate B => Car 5678 parked:", id, "err:", err)
	}()

	time.Sleep(time.Second * 2)
	parkingLot.DisplayAvailibilty()

	go func() {
		err := parkingLot.Exit(10)
		fmt.Println("Car exit spot 1 -> ", "err: ", err)

	}()
	time.Sleep(time.Second * 1)

}
